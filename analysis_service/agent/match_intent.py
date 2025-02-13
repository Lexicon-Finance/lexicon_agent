from langchain_openai import ChatOpenAI
from typing import Generator, Dict, Any

from agent.tools import tools
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
memory_saver = MemorySaver()
query = "Output your matching analysis in format: {title: Intent Match Report, match_score: <match_score>, analysis: <analysis>}"


def match_transaction_intent(
    intent: str,
    from_address: str,
    to_address: str,
    value: str,
    data: str,
    dataDecoded: str,
    gas: str = "0",
    gas_price: str = "0"
) -> Generator[Dict[str, Any], None, None]:
    """
    Given an intent description and transaction metadata, determine if they match.
    Returns a generator that yields conversation messages.
    
    Args:
        intent: Natural language description of intended transaction
        from_address: Sender's address
        to_address: Recipient's address
        value: Transaction value
        data: Transaction data
        dataDecoded: Transaction decoded data
        gas: Gas limit (optional)
        gas_price: Gas price (optional)
    """
    
    template = '''
    Analyze if the following transaction matches the stated intent.
    Use the available tools if necessary: RunSimulation, GetContractDetails, GetPastTransactions, Search, IdentifyAddressType.

    {tools}

    Intent Description:
    {intent}

    Transaction Metadata:
    from_address: {from_address}
    to_address: {to_address} 
    value: {value}
    data: {data}
    gas: {gas}
    gas_price: {gas_price}
    dataDecoded: {dataDecoded}

    Check steps:
    1. Understand the user's intent - what are they trying to achieve?
    2. Analyze the transaction details to determine what it actually does
    3. Run simulation if needed to verify transaction outcome
    4. Compare intended vs actual outcome

    context:
    1, from is user's address
    2, gas and gas_price are 0 by default
    
    
    Provide a match score between 0 (completely different) and 100 (perfect match) along with your reasoning.
    Explain any discrepancies between intent and actual transaction.
    '''
    
    prompt = template.format(
        tools=tools,
        intent=intent,
        from_address=from_address,
        to_address=to_address,
        value=value,
        data=data,
        gas=gas,
        gas_price=gas_price,
        dataDecoded=dataDecoded
    )
    
    agent_executor = create_react_agent(model, tools, prompt=prompt)
    stream = agent_executor.stream({"messages": [("human", query)]}, stream_mode="values")
    
    for s in stream:
        message = s["messages"][-1]
        yield {"content": message.pretty_repr()}
    
    #print_stream(stream)


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
    return message
