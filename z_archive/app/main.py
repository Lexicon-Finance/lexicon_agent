from fastapi import FastAPI
from app.intent_matcher import match_intent_with_transaction
from app.risk_detector import evaluate_transaction
from app.llm_handler import parse_llm_match_output

app = FastAPI()

@app.post("/analyze_transaction")
def analyze_transaction(intent: str, tx_data: dict):
    """
    Analyzes an Ethereum transaction for risks and checks if it matches intent.
    """
    # Step 1: Run Risk Detection
    risk_result = evaluate_transaction(tx_data)

    # Step 2: Run Intent Matching
    llm_response = match_intent_with_transaction(intent, tx_data)
    intent_result = parse_llm_match_output(llm_response)

    # Step 3: Return Combined Results
    return {
        "risk_analysis": risk_result,
        "intent_match": intent_result
    }
