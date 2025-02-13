#from risk_detect import analyze_transaction
from match_intent import match_transaction_intent

'''
def test_analyze_transaction():
    # Test transaction parameters
    from_address = "0x179a8BDDa1AB5fEF17AAF6Ff0FFCb2875925668F"
    to_address = "0x2F5213757a486C4DCDB4708AE53b834b9445bbA7" 
    value = "0"
    data = "0xa9059cbb0000000000000000000000006a9ee871c0bd10323121b1f0e9c7212c48695d9900000000000000000000000000000000000000000000152d02c7e14af6800000"
    
    # Call analyze_transaction
    result = analyze_transaction(
        from_address=from_address,
        to_address=to_address,
        value=value,
        data=data,
        gas="0",
        gas_price="0"
    )
    
    return result
'''

def test_match_intent():
    # Test transaction parameters
    intent = "Send 100 USDC to address 0x6a9ee871c0bd10323121b1f0e9c7212c48695d99"
    from_address = "0x179a8BDDa1AB5fEF17AAF6Ff0FFCb2875925668F"
    to_address = "0x2F5213757a486C4DCDB4708AE53b834b9445bbA7"  # USDC contract
    value = "0"
    data = "0xa9059cbb0000000000000000000000006a9ee871c0bd10323121b1f0e9c7212c48695d9900000000000000000000000000000000000000000000152d02c7e14af6800000"
    dataDecoded = 'transfer([ { "name": "to", "type": "address", "value": "0x6A9Ee871c0Bd10323121b1F0e9C7212c48695d99" }, { "name": "value", "type": "uint256", "value": "100000000000000000000000" } ])'
    # Call match_transaction_intent
    result = match_transaction_intent(
        intent=intent,
        from_address=from_address,
        to_address=to_address,
        value=value,
        data=data,
        dataDecoded=dataDecoded
    )
    
    return result

if __name__ == "__main__":
    # Test risk detection
    #risk_result = test_analyze_transaction()
    #print(f"Risk analysis result: {risk_result}")
    
    # Test intent matching
    test_match_intent()
    