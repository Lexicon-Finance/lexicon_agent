import requests
from app.config import TENDERLY_API_KEY

def simulate_transaction(tx_data):
    """
    Simulates an Ethereum transaction and returns the simulation result.
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
        "value": hex(int(tx_data["value"] * 1e18)),
        "gas": "0x5208",
        "gas_price": "0x3B9ACA00",
        "input": tx_data.get("data", "0x")
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def extract_risk_signals(simulation_response):
    """
    Extracts key risk factors from the simulated transaction.
    """
    risk_factors = []

    # Check if transaction failed
    if simulation_response.get("error"):
        risk_factors.append(f"Transaction failed: {simulation_response['error']}. Possible scam.")

    # Check if gas usage is unusually high
    gas_used = int(simulation_response.get("gas_used", "0"), 16)
    if gas_used > 500000:
        risk_factors.append("High gas usage detected. Possible contract exploit.")

    # Detect risky function calls
    for call in simulation_response.get("calls", []):
        if "approve" in call.get("function", "").lower():
            risk_factors.append("Transaction calls `approve()`. This could be a phishing attempt.")

    return risk_factors

def evaluate_transaction(tx_data):
    """
    Evaluates a transaction by simulating it and extracting risk factors.
    """
    simulation = simulate_transaction(tx_data)
    risk_signals = extract_risk_signals(simulation)
    return {"simulation": simulation, "risks": risk_signals}
