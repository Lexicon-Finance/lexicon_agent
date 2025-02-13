from fastapi import APIRouter, HTTPException
from services.sign_transaction import send_safe_transaction
from fastapi.params import Query

api_router = APIRouter()

@api_router.post("/send_safe_transaction/")
async def send_transaction(safe_tx_hash: str = Query(...), safe_address: str = Query(...)):
    """
    Endpoint to send a Safe multisig transaction.
    """
    try:
        result = send_safe_transaction(safe_tx_hash=safe_tx_hash, safe_address=safe_address)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Explicitly export the router
__all__ = ['api_router']