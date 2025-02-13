from typing import Dict, Any, List
from dataclasses import dataclass
import json

@dataclass
class TransactionData:
    from_address: str
    to_address: str
    value: int
    input_data: str
    gas: int
    gas_price: int

@dataclass
class SimulationResult:
    state_changes: List[Dict[str, Any]]
    token_transfers: List[Dict[str, Any]]
    balance_changes: List[Dict[str, Any]]
    logs: List[Dict[str, Any]]

class LLMIntentMatcher:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def match_intent(
        self,
        transaction: TransactionData,
        simulation: SimulationResult,
        user_intent: str
    ) -> bool:
        """
        Use LLM to match the transaction and simulation against the user's stated intent
        
        Args:
            transaction: The EVM transaction data
            simulation: The Tenderly simulation result
            user_intent: Natural language description of user's intended action
            
        Returns:
            bool: True if the transaction matches the intent, False otherwise
        """
        # Create a structured description of the transaction effects
        transaction_effects = self._get_transaction_effects(transaction, simulation)
        
        # Construct the prompt for the LLM
        prompt = self._construct_prompt(transaction_effects, user_intent)
        
        # Get LLM's analysis
        response = self.llm_client.analyze(prompt)
        
        # Parse the response to get the final true/false result
        return self._parse_llm_response(response)

    def _get_transaction_effects(
        self,
        transaction: TransactionData,
        simulation: SimulationResult
    ) -> Dict[str, Any]:
        """
        Extract and structure the effects of the transaction from simulation results
        """
        effects = {
            "token_transfers": [],
            "balance_changes": [],
            "state_changes": [],
            "transaction_details": {
                "from": transaction.from_address,
                "to": transaction.to_address,
                "value": transaction.value,
            }
        }

        # Process token transfers
        for transfer in simulation.token_transfers:
            effects["token_transfers"].append({
                "token": transfer["token_address"],
                "from": transfer["from"],
                "to": transfer["to"],
                "amount": transfer["amount"],
                "symbol": transfer.get("symbol", "UNKNOWN")
            })

        # Process balance changes
        for change in simulation.balance_changes:
            effects["balance_changes"].append({
                "address": change["address"],
                "delta": change["delta"],
                "token": change.get("token", "ETH")
            })

        return effects

    def _construct_prompt(
        self,
        transaction_effects: Dict[str, Any],
        user_intent: str
    ) -> str:
        """
        Construct a prompt for the LLM to analyze the transaction
        """
        prompt = f"""
        Task: Analyze if the following blockchain transaction matches the user's stated intent.

        User's Intent:
        {user_intent}

        Transaction Effects:
        {json.dumps(transaction_effects, indent=2)}

        Please analyze if the transaction effects match the user's stated intent.
        Consider:
        1. Token transfers and their amounts
        2. Balance changes
        3. Direction of transfers (from/to addresses)
        4. Any relevant state changes

        Respond with a JSON object containing:
        {{
            "matches_intent": true/false,
            "explanation": "Detailed explanation of why it matches or doesn't match",
            "confidence": 0-100
        }}
        """
        return prompt

    def _parse_llm_response(self, response: str) -> bool:
        """
        Parse the LLM's response to determine if the transaction matches the intent
        """
        try:
            result = json.loads(response)
            # Only return true if the match is confident (>80%) and positive
            return (
                result.get("matches_intent", False) and 
                result.get("confidence", 0) > 80
            )
        except json.JSONDecodeError:
            return False

    def _format_amount(self, amount: int, decimals: int = 18) -> str:
        """Helper method to format token amounts with proper decimals"""
        return str(amount / (10 ** decimals))

    def _get_token_symbol(self, address: str) -> str:
        """Helper method to get token symbol from address"""
        # This could be implemented to lookup token symbols from a token database
        return f"TOKEN({address[:6]}...{address[-4:]})"
