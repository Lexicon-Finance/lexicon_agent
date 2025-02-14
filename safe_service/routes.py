from fastapi import APIRouter, HTTPException
from services.sign_transaction import send_safe_transaction

api_router = APIRouter()

@api_router.post("/send_safe_transaction/{safe_address}/{safe_tx_hash}")
async def send_transaction(safe_address: str, safe_tx_hash: str):
    """
    Endpoint to send a Safe multisig transaction.
    
    Parameters:
        safe_address: The address of the Safe contract
        safe_tx_hash: The hash of the transaction to be executed
    """
    try:
        result = send_safe_transaction(safe_tx_hash=safe_tx_hash, safe_address=safe_address)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Explicitly export the router
__all__ = ['api_router']