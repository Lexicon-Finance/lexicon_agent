import sys
import os
import json
import asyncio

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from analysis_service.services.risk_detector import RiskDetector

def load_json(filename):
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, '..', 'jsons', filename)
    with open(json_path, 'r') as f:
        return json.load(f)

async def test_risk_detector():
    # Load test data
    contract_abi = load_json('contract_abi.json')
    tx_data = load_json('tx_data.json')
    decoded_tx = load_json('decoded_tx.json')
    simulation = load_json('simulation.json')

    # Convert contract ABI to the expected format
    contract_abi_dict = {
        "abi": contract_abi,
        "contractName": "DummyUSDT",
        "address": tx_data["to"]
    }

    # Initialize risk detector
    risk_detector = RiskDetector()
    
    # Call detect_risks with the test data
    risks = await risk_detector.detect_risks(
        contract_abi=contract_abi_dict,
        #tx_metadata=tx_data,
        decoded_tx=decoded_tx,
        contract_name="DummyUSDT",
        simulation_result=simulation
    )

    print(risks)

if __name__ == "__main__":
    asyncio.run(test_risk_detector())