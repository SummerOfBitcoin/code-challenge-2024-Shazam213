import json
import os
import hashlib

# Constants
DIFFICULTY_TARGET = "0000ffff00000000000000000000000000000000000000000000000000000000"
BLOCK_SIZE_LIMIT = 4000000  # Assuming block size limit is 4,000,000 bytes

# Validate a transaction
def validate_transaction(transaction):
    # Implement your validation logic here
    return True  # Placeholder, actual validation needed

# Read transactions from the mempool folder
mempool_folder = "mempool"
transactions = []
for filename in os.listdir(mempool_folder):
    if filename.endswith(".json"):
        with open(os.path.join(mempool_folder, filename)) as file:
            transaction_data = json.load(file)
            transactions.append(transaction_data)

# Validate transactions and filter valid ones
valid_transactions = [tx for tx in transactions if validate_transaction(tx)]

# Sort valid transactions by fee in descending order
# Sort valid transactions by fee in descending order
valid_transactions.sort(key=lambda x: x.get("fee", 0), reverse=True)


# Calculate total fee and block size
total_fee = 0
block_size = 0
for tx in valid_transactions:
    try:
        total_fee += tx["fee"]
        block_size += len(json.dumps(tx))
    except KeyError:
        pass  # Ignore transactions without a fee field
# total_fee = sum(tx["fee"] for tx in valid_transactions)
# block_size = sum(len(json.dumps(tx)) for tx in valid_transactions)
mined_transactions = []

# Create the block header
block_header = {
    "previous_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "merkle_root": "merkle_root_placeholder",
    "timestamp": "timestamp_placeholder",
    "bits": DIFFICULTY_TARGET,
    "nonce": 0
}

# Create the coinbase transaction
coinbase_transaction = {
    "txid": "coinbase",
    "vin": [],
    "vout": [{"value": total_fee, "scriptpubkey_asm": "coinbase_script"}]
}

# Mine the block
while True:
    block_data = json.dumps([block_header, coinbase_transaction] + mined_transactions)
    block_hash = hashlib.sha256(block_data.encode()).hexdigest()
    if block_hash[:16] == DIFFICULTY_TARGET:
        break
    block_header["nonce"] += 1

# Write the output file
with open("output.txt", "w") as output_file:
    output_file.write(f"Block Header: {json.dumps(block_header)}\n")
    output_file.write(f"Coinbase Transaction: {json.dumps(coinbase_transaction)}\n")
    output_file.write(f"Transactions:\n")
    for transaction in mined_transactions:
        output_file.write(f"{transaction['txid']}\n")
