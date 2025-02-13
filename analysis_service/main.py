from fastapi import FastAPI, HTTPException
from typing import Dict, Any
#from services.llm_handler import LLMHandler
#from services.intent_matcher import IntentMatcher
from services.risk_detector import RiskDetector
from services.simulation_handler import simulate_transaction
from fastapi.middleware.cors import CORSMiddleware
from services.etherscan_service import EtherscanService
from fastapi.responses import StreamingResponse
from agent.risk_detect import analyze_transaction
from agent.match_intent import match_transaction_intent
import json

app = FastAPI(title="Analysis Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
etherscan_service = EtherscanService()
'''
# Initialize services
llm_handler = LLMHandler()
intent_matcher = IntentMatcher()
risk_detector = RiskDetector()

# Inject dependencies
intent_matcher.llm_handler = llm_handler
risk_detector.llm_handler = llm_handler



@app.post("/analyze")
async def analyze_transaction(transaction_data: Dict[str, Any]):
    try:
        # Match transaction intent
        intent = await intent_matcher.match_intent(transaction_data)
        
        # Detect risks
        risk_score, risk_factors = await risk_detector.detect_risks(transaction_data)
        
        return {
            "transaction_id": transaction_data.get("id"),
            "intent": intent.value,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "is_risky": risk_score > settings.RISK_THRESHOLD
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''

@app.post("/simulate")
async def simulate(
    from_address: str,
    to_address: str,
    value: int = 0,
    gas: int = 0,
    gas_price: int = 0,
    input: str = "0x"
):
    """
    Endpoint to simulate an Ethereum transaction.
    
    Parameters:
        from_address: str - Sender address (0x...)
        to_address: str - Recipient address (0x...)
        value: int - Transaction value in wei (optional)
        gas: int - Gas limit (optional)
        gas_price: int - Gas price in wei (optional)
        input: str - Transaction input data as hex string (optional)
    """
    try:
        transaction_data = {
            "from": from_address,
            "to": to_address,
            "value": value,
            "gas": gas,
            "gas_price": gas_price,
            "input": input
        }
        
        simulation_result = simulate_transaction(transaction_data)
        return {
            "status": "success",
            "simulation_result": simulation_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contract/{contract_address}")
async def get_contract_info(contract_address: str):
    """
    Endpoint to fetch contract name and ABI from Etherscan
    
    Parameters:
        contract_address: str - Contract address to query (0x...)
    """
    try:
        contract_name, contract_abi = await etherscan_service.get_contract_info(contract_address)
        
        if not contract_name:
            raise HTTPException(
                status_code=404,
                detail="Contract not found or not verified on Etherscan"
            )
            
        return {
            "status": "success",
            "contract_name": contract_name,
            "contract_abi": contract_abi
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze(
    from_address: str,
    to_address: str,
    value: str = "0",
    data: str = "0x",
    gas: str = "0",
    gas_price: str = "0",
    dataDecoded: str = ""
):
    """
    Endpoint to analyze a transaction and stream the conversation.
    
    Parameters:
        from_address: str - Sender address (0x...)
        to_address: str - Recipient address (0x...)
        value: str - Transaction value
        data: str - Transaction input data
        gas: str - Gas limit (optional)
        gas_price: str - Gas price (optional)
    """
    try:
        def generate():
            for message in analyze_transaction(
                from_address=from_address,
                to_address=to_address,
                value=value,
                data=data,
                gas=gas,
                gas_price=gas_price,
                dataDecoded=dataDecoded
            ):
                yield f"data: {json.dumps(message)}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match-intent")
async def match_intent(
    intent: str,
    from_address: str,
    to_address: str,
    value: str = "0",
    data: str = "0x",
    gas: str = "0",
    gas_price: str = "0",
    dataDecoded: str = ""
):
    """
    Endpoint to match transaction against stated intent and stream the analysis.
    
    Parameters:
        intent: str - Natural language description of intended transaction
        from_address: str - Sender address (0x...)
        to_address: str - Recipient address (0x...)
        value: str - Transaction value
        data: str - Transaction input data
        gas: str - Gas limit (optional)
        gas_price: str - Gas price (optional)
        dataDecoded: str - Decoded transaction data (optional)
    """
    try:
        def generate():
            for message in match_transaction_intent(
                intent=intent,
                from_address=from_address,
                to_address=to_address,
                value=value,
                data=data,
                gas=gas,
                gas_price=gas_price,
                dataDecoded=dataDecoded
            ):
                yield f"data: {json.dumps(message)}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
