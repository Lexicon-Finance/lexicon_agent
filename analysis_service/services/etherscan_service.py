import os
import aiohttp
from typing import Optional, Tuple

class EtherscanService:
    def __init__(self):
        self.api_key = "BS6G99G2CRZKRGXJ2PFM9WEDVP33PEEY86"
        self.base_url = os.getenv("ETHERSCAN_URL", "https://api-sepolia.etherscan.io/api")
        
        if not self.api_key:
            raise ValueError("ETHERSCAN_API_KEY environment variable is not set")

    async def get_contract_info(self, contract_address: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Fetches contract name and ABI from Etherscan
        
        Args:
            contract_address: The contract address to query
            
        Returns:
            Tuple containing (contract_name, contract_abi)
            If contract is not verified, returns (None, None)
        """
        timeout = aiohttp.ClientTimeout(total=30)  # 30 seconds timeout
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Get contract name
            params = {
                'module': 'contract',
                'action': 'getsourcecode',
                'address': contract_address,
                'apikey': self.api_key
            }
            
            try:
                async with session.get(self.base_url, params=params, ssl=False) as response:
                    if response.status != 200:
                        print(f"Error response from Etherscan: {response.status}")
                        return None, None
                        
                    data = await response.json()
                    print(f"Source code response: {data}")  # Debug print
                    
                    if data.get('status') != '1' or not data.get('result', [{}])[0].get('ContractName'):
                        return None, None
                        
                    contract_name = data['result'][0]['ContractName']
                    
                    # Get contract ABI
                    abi_params = {
                        'module': 'contract',
                        'action': 'getabi',
                        'address': contract_address,
                        'apikey': self.api_key
                    }
                    
                    async with session.get(self.base_url, params=abi_params, ssl=False) as abi_response:
                        if abi_response.status != 200:
                            print(f"Error response from Etherscan ABI endpoint: {abi_response.status}")
                            return contract_name, None
                            
                        abi_data = await abi_response.json()
                        print(f"ABI response: {abi_data}")  # Debug print
                        
                        if abi_data.get('status') != '1':
                            return contract_name, None
                            
                        contract_abi = abi_data['result']
                        
                        return contract_name, contract_abi
                    
            except aiohttp.ClientError as e:
                print(f"Error fetching contract info: {str(e)}")
                return None, None
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return None, None 