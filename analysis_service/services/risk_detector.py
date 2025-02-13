from typing import Dict, Any, List, Tuple, Optional
#from config import MAX_TRANSACTION_AMOUNT
from .llm_handler import LLMHandler

class RiskDetector:
    def __init__(self):
        self.llm_handler = LLMHandler() 
    
    def _prepare_llm_prompt(self, 
                          #tx_metadata: Dict[str, Any],
                          simulation_result: Dict[str, Any],
                          decoded_tx: Dict[str, Any],
                          contract_name: str,
                          contract_abi: Dict[str, Any]) -> str:
        """
        Prepare a prompt for the LLM to analyze transaction risks.
        """
        prompt = f"""Analyze the following smart contract transaction for potential risks:


Simulation Result:
{simulation_result}

Decoded Transaction:
{decoded_tx}

Contract Name: {contract_name}

Contract ABI:
{contract_abi}

Please analyze this transaction for potential risks and provide:
1. A risk score between 0.0 (safe) and 1.0 (high risk)
2. A detailed list of risk factors identified
3. Explanation of the risk score. if the score<0.5, explain why it is low-risk, if the score>0.5 explain why it is high-risk.

Format your response as JSON with the following structure:
{{
    "risk_score": float,
    "risk_factors": [string],
    "risk_analysis": string
}}
"""
        return prompt

    def _transform_json_inputs(self, 
                             #tx_metadata: Any,
                             simulation_result: Any,
                             decoded_tx: Any,
                             contract_abi: Any) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """
        Transform JSON string inputs into Python dictionaries if needed.
        
        Args:
            tx_metadata: Transaction metadata (JSON string or dict)
            simulation_result: Simulation results (JSON string or dict)
            decoded_tx: Decoded transaction (JSON string or dict)
            contract_abi: Contract ABI (JSON string or dict)
            
        Returns:
            Tuple of transformed dictionaries
        """
        import json

        def parse_json(data: Any) -> Dict[str, Any]:
            if isinstance(data, str):
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON string: {data}")
            elif isinstance(data, dict):
                return data
            else:
                raise ValueError(f"Input must be JSON string or dict, got {type(data)}")

        return (
            #parse_json(tx_metadata),
            parse_json(simulation_result),
            parse_json(decoded_tx),
            parse_json(contract_abi)
        )

    async def detect_risks(self,
                          simulation_result: Any,
                          decoded_tx: Any,
                          contract_name: str,
                          contract_abi: Any) -> Tuple[float, List[str]]:
        """
        Detect potential risks in a transaction using both rule-based checks and LLM analysis.
        
        Args:
            tx_metadata: Transaction metadata (JSON string or dict)
            simulation_result: Results from transaction simulation (JSON string or dict)
            decoded_tx: Decoded transaction details (JSON string or dict)
            contract_name: Name of the contract being interacted with
            contract_abi: ABI of the contract (JSON string or dict)
        """
        # Transform JSON inputs to dictionaries
        try:
            simulation_result_dict, decoded_tx_dict, contract_abi_dict = \
                self._transform_json_inputs(simulation_result, decoded_tx, contract_abi)
        except ValueError as e:
            return 1.0, [f"Input validation failed: {str(e)}"]

        llm_risk_score = 0.0
        llm_risk_factors = []
        
        # LLM-based analysis
        if self.llm_handler:
            prompt = self._prepare_llm_prompt(
                simulation_result_dict,
                decoded_tx_dict,
                contract_name,
                contract_abi_dict
            )
            
            try:
                llm_response = await self.llm_handler.analyze(prompt)
                
                llm_risk_score = llm_response.get("risk_score", 0.0)
                llm_risk_factors = llm_response.get("risk_factors", [])
                llm_risk_analysis = llm_response.get("risk_analysis", "")
                
            except Exception as e:
                llm_risk_factors.append(f"LLM analysis failed: {str(e)}")
        
        # Ensure risk score is between 0 and 1
        llm_risk_score = max(0.0, min(1.0, llm_risk_score))
        
        return llm_risk_score, llm_risk_factors, llm_risk_analysis