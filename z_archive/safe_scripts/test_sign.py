from sign_transaction import send_safe_transaction, TransactionDetails
from hexbytes import HexBytes


tx = TransactionDetails(
    safe_address="0xYourSafeAddress",
    to_address="0xRecipientAddress",
    value=1000000000000000000  # 1 ETH in Wei
)

safe_address = '0x179a8BDDa1AB5fEF17AAF6Ff0FFCb2875925668F'
safe_tx = '0xc6006f6e2302f0d48c5c6c3867e29540fa053190d1c6990f624f2eec7372cf22'
print(safe_tx)

result = send_safe_transaction(safe_tx,safe_address)
print(result)