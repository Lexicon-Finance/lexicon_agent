from app.llm_handler import call_llm

def match_intent_with_transaction(intent_description, transaction_data):
    """
    Uses an LLM to determine if a transaction matches a user's intent.
    """

    prompt = f"""
    You are an Ethereum transaction intent verification assistant.
    
    **User Intent:** "{intent_description}"

    **Transaction Details:**
    - From: {transaction_data.get("from")}
    - To: {transaction_data.get("to")}
    - Value: {transaction_data.get("value")} ETH
    - Function Called: {transaction_data.get("function_name", "Unknown")}
    - Gas Used: {transaction_data.get("gas_used", "Unknown")}

    **Task:**
    - Assign a match percentage (0-100%) based on correctness.
    - Explain any discrepancies in the transaction.

    **Response Format:**
    ```
    Match Score: X%
    Explanation: "..."
    ```
    """
    return call_llm(prompt)
