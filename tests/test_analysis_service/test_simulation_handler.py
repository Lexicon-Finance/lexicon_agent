import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from analysis_service.services.simulation_handler import simulate_transaction

def test_simulate_transaction():
    tx_data = {
        "from": "0x179a8BDDa1AB5fEF17AAF6Ff0FFCb2875925668F",
        "to": "0xAe473fD3640423d6Fa3C3558F35f9De2FbFF54E7",
        "value": 100
    }
    result = simulate_transaction(tx_data)
    print(result)

if __name__ == "__main__":
    test_simulate_transaction()