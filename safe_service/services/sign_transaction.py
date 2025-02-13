import os
import logging
from dataclasses import dataclass
#from dotenv import load_dotenv
from config import RPC_URL, OWNER_A_PRIVATE_KEY
from safe_eth.eth import EthereumClient, EthereumNetwork
from safe_eth.safe.api.transaction_service_api import TransactionServiceApi
from safe_eth.safe import Safe
from hexbytes import HexBytes


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
#load_dotenv()

@dataclass
class TransactionDetails:
    """Encapsulates all transaction details."""
    safe_address: str  # The Safe contract address
    to_address: str  # The recipient's Ethereum address
    value: int  # Amount to send in Wei
    data: str = "0x"  # Default empty data field
    gas_price: int = None  # Optional gas price (Wei)
    gas_limit: int = None  # Optional gas limit

async def send_safe_transaction(safe_tx_hash: str, safe_address: str):
    """
    Sends a Safe multisig transaction using structured TransactionDetails.

    Parameters:
    - tx_details (TransactionDetails): The transaction details object.

    Returns:
    - dict: Transaction response or error message.
    """

    #RPC_URL = os.getenv("RPC_URL")
    #OWNER_A_PRIVATE_KEY = os.getenv("OWNER_A_PRIVATE_KEY")
    SAFE_ADDRESS = safe_address
    safe_tx_hash_hex = HexBytes(safe_tx_hash)
    
    logging.info(f"Connecting to Ethereum network via {RPC_URL}")
    ethereum_client = EthereumClient(RPC_URL)

        # Instantiate a Safe contract instance
    safe = Safe(SAFE_ADDRESS, ethereum_client)

        # Create a Safe transaction
    #safe_tx = safe.build_multisig_tx(
   #         tx_details.to_address,
   #         tx_details.value,
   #         HexBytes(tx_details.data),
   #         gas_price=tx_details.gas_price,
    #        gas_limit=tx_details.gas_limit
     #   )

         # Instantiate the Transaction Service API
    transaction_service_api = TransactionServiceApi(
            network=EthereumNetwork.SEPOLIA,  # Ensure this matches your network
            ethereum_client=ethereum_client
    
    )

    (safe_tx, _) = transaction_service_api.get_safe_transaction(safe_tx_hash_hex)

    # Sign the transaction with Owner A
    safe_tx.sign(OWNER_A_PRIVATE_KEY)
    logging.info("Transaction signed successfully.")

    

    # Send the transaction to the Transaction Service
    response = transaction_service_api.post_transaction(safe_tx)

    logging.info("Transaction sent successfully!")
    return {"status": "success", "response": response}

# Explicitly export the function
__all__ = ['send_safe_transaction']
