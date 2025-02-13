import json
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from analysis_service.services.simulation_handler import simulate_transaction
from langchain_community.utilities import GoogleSerperAPIWrapper
from web3 import Web3

os.environ["SERPER_API_KEY"] = "3198e2470fff9f05af9cc53a0c90bf557ed78eb2"


def run_simulation_tool(input_data: str) -> str:
    """
    Simulate the transaction behavior based on input metadata.
    Uses the simulation_handler to simulate transaction execution.
    """
    
    try:
        # Parse input string to dict
        tx_data = json.loads(input_data)
        
        # Prepare transaction data for simulation
        simulation_data = {
            "from": tx_data.get("from", ""),
            "to": tx_data.get("to", ""),
            "value": int(tx_data.get("value", 0)),
            "gas": int(tx_data.get("gas", 0)), 
            "gas_price": int(tx_data.get("gasPrice", 0)),
            "input": tx_data.get("data", "0x")
        }

        # Use simulation handler to run simulation
        
        result = simulate_transaction(simulation_data)
        
        return json.dumps(result)

    except Exception as e:
        return f"Error running simulation: {str(e)}"

def get_contract_details_tool(input_data: str) -> str:
    """
    Retrieve details about a contract given its address.
    In practice, you might query a blockchain explorer or use an API.
    """
    try:
        # Prepare API request
        api_key = "BS6G99G2CRZKRGXJ2PFM9WEDVP33PEEY86"  # Using key from etherscan_service.py
        url = f"https://api-sepolia.etherscan.io/api?module=contract&action=getsourcecode&address={input_data}&apikey={api_key}"
        
        # Make request
        import requests
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            return f"Error fetching contract details: {response.status_code}"
            
        data = response.json()
        
        if data.get('status') != '1':
            return f"Contract not found or error: {data.get('message')}"
            
        result = data['result'][0]
        contract_name = result.get('ContractName', 'Unknown')
        verified = "Verified" if result.get('ContractName') else "Unverified"
        
        return f"Contract {contract_name} at {input_data}: {verified} with source code: {result.get('SourceCode', 'No source code available')} and abi: {result.get('ABI', 'No ABI available')}"
        
    except Exception as e:
        return f"Error fetching contract details: {str(e)}"

def get_past_transaction_tool(input_data: str) -> str:
    """
    Get past transactions for a given address.
    """
    try:
        # Prepare API request
        api_key = "BS6G99G2CRZKRGXJ2PFM9WEDVP33PEEY86"
        url = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={input_data}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}"
        
        # Make request
        import requests
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            return f"Error fetching transactions: {response.status_code}"
            
        data = response.json()
        
        if data.get('status') != '1':
            return f"No transactions found or error: {data.get('message')}"
            
        # Get the 5 most recent transactions
        recent_txs = data['result'][:5]
        
        # Format transaction details
        tx_details = []
        for tx in recent_txs:
            tx_details.append(
                f"Hash: {tx.get('hash')}\n"
                f"From: {tx.get('from')}\n"
                f"To: {tx.get('to')}\n" 
                f"Value: {tx.get('value')} Wei\n"
                f"Block: {tx.get('blockNumber')}\n"
                f"---"
            )
            
        return "\n".join(tx_details)
        
    except Exception as e:
        return f"Error fetching transactions: {str(e)}"

def search_tool(input_data: str) -> str:
    """
    Perform an external search (e.g., for news or security alerts) based on a query.
    """
    serper_api_wrapper = GoogleSerperAPIWrapper()
    # In a real implementation, you might search a news API or database.
    return serper_api_wrapper.run(input_data)

def identify_address_type_tool(input_data: str) -> str:
    """
    Identify if an address is an EOA (Externally Owned Account) or a smart contract.
    Uses Web3 to check if there's contract code at the address.
    """
    try:
        # Initialize Web3 with Sepolia provider
        w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/demo'))
        
        # Check if the address is valid
        if not w3.is_address(input_data):
            return f"Error: {input_data} is not a valid Ethereum address"
            
        # Get the contract code at the address
        code = w3.eth.get_code(input_data)
        
        # If there's no code (just '0x'), it's an EOA
        if code == b'':  # or hex(code) == '0x'
            return f"Address {input_data} is an Externally Owned Account (EOA)"
        else:
            return f"Address {input_data} is a Smart Contract"
        
    except Exception as e:
        return f"Error checking address type: {str(e)}"

from langchain.agents import Tool

tools = [
    Tool(
        name="RunSimulation",
        func=run_simulation_tool,
        description=(
            "Simulate the transaction behavior to check for abnormal activity. "
            "Input should be the transaction metadata as a json string."
            "Input format should be like this: {'from': '0x123', 'to': '0x456', 'value': 100, 'gas': 21000, 'gasPrice': 1000000000, 'data': '0x1234567890abcdef'}"
        )
    ),
    Tool(
        name="GetContractDetails",
        func=get_contract_details_tool,
        description=(
            "Fetch details about a smart contract given its address. "
            "Input: contract address (string)."
        )
    ),
    Tool(
        name="GetPastTransactions",
        func=get_past_transaction_tool,
        description=(
            "Get past transactions for a given address. "
            "Input: address (string)."
        )
    ),
    Tool(
        name="Search",
        func=search_tool,
        description=(
            "Perform a search for additional context (such as news or alerts) about "
            "the transaction or contract. Input: query string."
        )
    ),
    Tool(
        name="IdentifyAddressType",
        func=identify_address_type_tool,
        description=(
            "Identify if an address is an EOA (Externally Owned Account) or a smart contract. "
            "Input: Ethereum address (string)."
        )
    )
]
