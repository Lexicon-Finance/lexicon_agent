import requests
#from config import TENDERLY_API_KEY

TENDERLY_API_KEY = "X2-Yi10WYZX5pywj0ZEclz097z9FcHte"

def simulate_transaction(tx_data):
    """
    Simulates an Ethereum transaction and returns the simulation result.
    
    Args:
        tx_data (dict): Transaction data containing:
            - from (str): Sender address
            - to (str): Recipient address
            - value (int): Transaction value in wei
            - gas (int): Gas limit
            - gas_price (int): Gas price in wei
            - input (str): Transaction input data (hex string)
    
    Returns:
        dict: Simulation response from Tenderly API
    """
    url = "https://api.tenderly.co/api/v1/account/rex_lee_hype/project/project/simulate"
    
    headers = {
        "Content-Type": "application/json",
        "X-Access-Key": TENDERLY_API_KEY
    }
    
    payload = {
        "network_id": "11155111",
        "from": tx_data["from"],
        "to": tx_data["to"],
        "value": tx_data.get("value", 0),
        "gas": tx_data.get("gas", 0),
        "gas_price": tx_data.get("gas_price", 0),
        "input": tx_data.get("input", "0x"),
        "simulation_type": "quick"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()