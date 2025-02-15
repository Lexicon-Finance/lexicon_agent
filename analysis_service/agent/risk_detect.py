from langchain_openai import ChatOpenAI
from typing import Generator, Dict, Any

from agent.tools import tools
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
memory_saver = MemorySaver()
query = "Output the risk score and your analysis in format: {title: Risk Report, risk_score: <risk_score>, analysis: <analysis>}"


def analyze_transaction(
    from_address: str,
    to_address: str,
    value: str,
    data: str,
    dataDecoded: str,
    gas: str = "0", 
    gas_price: str = "0"
) -> Generator[Dict[str, Any], None, None]:
    """
    Given transaction metadata, construct a prompt and use the agent to analyze the risk.
    Returns a generator that yields conversation messages.
    """
    
    template = '''
    You are expert of risk detection on EVM transactions. Analyze the following transaction deeply and determine its risk level.
    Use the available tools if necessary: RunSimulation, GetContractDetails, GetPastTransactions, Search, IdentifyAddressType.

    {tools}

    Transaction Metadata:
    from_address: {from_address}
    to_address: {to_address} 
    value: {value}
    data: {data}
    gas: {gas}
    gas_price: {gas_price}
    dataDecoded: {dataDecoded}

    general rules of a good transaction:
    1,addresses in datadecoded are verified
    2,no malicious addresses in to_address or dataDecoded


    Context:
    1, the transaction is initiated from a safe wallet, there's no need checking the from address.
    2, gas and gas price are 0 becasue it is a safe tx.
    
    Provide a final risk score between 0 (low risk) and 100 (high risk) along with comprehensive analysis.
    '''
    
    prompt = template.format(
        tools=tools,
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

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
    return message


