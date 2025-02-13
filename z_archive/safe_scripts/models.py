from pydantic import BaseModel

class TransactionRequest(BaseModel):
    safe_tx_hash: str
    safe_address: str
