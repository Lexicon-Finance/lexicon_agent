import pytest
import asyncio
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from analysis_service.services.etherscan_service import EtherscanService

@pytest.mark.asyncio
async def test_etherscan_service():
    etherscan_service = EtherscanService()
    
    # Test with a known verified contract on Sepolia
    # Using USDC contract on Sepolia as an example
    contract_address = '0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238'
    
    print(f"\nTesting with contract address: {contract_address}")
    contract_name, contract_abi = await etherscan_service.get_contract_info(contract_address)
    
    print(f"Retrieved contract name: {contract_name}")
    print(f"Retrieved ABI: {'<available>' if contract_abi else '<none>'}")
    
    assert contract_name is not None, "Contract name should not be None for verified contract"
    assert contract_abi is not None, "Contract ABI should not be None for verified contract"
    
    # Test with an invalid contract address
    invalid_address = '0x1234567890123456789012345678901234567890'
    print(f"\nTesting with invalid address: {invalid_address}")
    invalid_name, invalid_abi = await etherscan_service.get_contract_info(invalid_address)
    
    print(f"Retrieved invalid contract name: {invalid_name}")
    print(f"Retrieved invalid ABI: {invalid_abi}")
    
    assert invalid_name is None, "Contract name should be None for invalid contract"
    assert invalid_abi is None, "Contract ABI should be None for invalid contract"

if __name__ == "__main__":
    asyncio.run(test_etherscan_service())