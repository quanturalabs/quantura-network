# sdk/cli.py

from web3 import Web3
import sys
import json

# --- Setup ---
RPC_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # or testnet
CONTRACT_ADDRESS = "0xYourOracleContractAddress"
ABI = json.loads("""[
    {
        "inputs":[{"internalType":"bytes32","name":"dataHash","type":"bytes32"}],
        "name":"submitResult",
        "outputs":[],
        "stateMutability":"nonpayable",
        "type":"function"
    },
    {
        "inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],
        "name":"getResult",
        "outputs":[
            {
                "components":[
                    {"internalType":"address","name":"submitter","type":"address"},
                    {"internalType":"bytes32","name":"dataHash","type":"bytes32"},
                    {"internalType":"uint256","name":"timestamp","type":"uint256"}
                ],
                "internalType":"struct QuanturaOracle.Result",
                "name":"",
                "type":"tuple"
            }
        ],
        "stateMutability":"view",
        "type":"function"
    }
]""")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# --- CLI Logic ---
def submit(data: str, private_key: str):
    acct = w3.eth.account.from_key(private_key)
    data_hash = Web3.keccak(text=data)
    txn = contract.functions.submitResult(data_hash).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })
    signed = acct.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("✅ Submitted! Tx hash:", tx_hash.hex())

def get_result(id: int):
    result = contract.functions.getResult(id).call()
    print("📦 Submitter:", result[0])
    print("🔐 Hash:", result[1].hex())
    print("⏱️ Timestamp:", result[2])

# --- Command-line interface ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cli.py submit 'some data' <private_key>")
        print("  python cli.py get 1")
        sys.exit(1)

    if sys.argv[1] == "submit":
        submit(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "get":
        get_result(int(sys.argv[2]))
    else:
        print("Unknown command")
