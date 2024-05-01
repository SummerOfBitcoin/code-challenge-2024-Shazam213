# import hashlib
# import json
# from ecdsa import VerifyingKey, BadSignatureError, SECP256k1

# message = bytes.fromhex('1764c3596c9499e1e5420a547a594874f2ec97589208cc62a580ebf27a33fa14')
# signature = bytes.fromhex('451008b776cb507dcdb1ad15bf5c0555add8e8c839ff146e73122c328105c45900923813f4487b624d1bf98e49ab9da9f2b3dc081e3c11fbf7070439787c2aaa')
# public_key = bytes.fromhex('03bea5d859ec5d95c449c736a0f19a5e52fdacf8b6b96afeaa415cd49f11e6a07c')

# vk = VerifyingKey.from_string(public_key, curve=SECP256k1)
# if vk.verify(signature, message, hashlib.sha256):
#     print("Signature is valid.")
# else:
#     print("Signature is not valid.")
from bitcoinlib.transactions import Tx, TxIn, TxOut
from bitcoinlib.keys import Address

# Transaction JSON
transaction_json = {
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "d1283ec7f6a2bcb65a5905033168258ca282e806c9dc7164415519a5ef041b14",
      "vout": 0,
      "prevout": {
        "scriptpubkey": "76a91496bc8310635539000a65a7cc95cb773c0cc7009788ac",
        "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 96bc8310635539000a65a7cc95cb773c0cc70097 OP_EQUALVERIFY OP_CHECKSIG",
        "scriptpubkey_type": "p2pkh",
        "scriptpubkey_address": "1Ek2BpKHUbr6SrrWq4P3Tf2jB6UCST2bwx",
        "value": 1103367
      },
      "scriptsig": "4730440220200b9a61529151f9f264a04e9aa17bb6e1d53fb345747c44885b1e185a82c17502200e41059f8ab4d3b3709dcb91b050c344b06c5086f05598d62bc06a8b746db4290121025f0ba0cdc8aa97ec1fffd01fac34d3a7f700baf07658048263a2c925825e8d33",
      "scriptsig_asm": "OP_PUSHBYTES_71 30440220200b9a61529151f9f264a04e9aa17bb6e1d53fb345747c44885b1e185a82c17502200e41059f8ab4d3b3709dcb91b050c344b06c5086f05598d62bc06a8b746db42901 OP_PUSHBYTES_33 025f0ba0cdc8aa97ec1fffd01fac34d3a7f700baf07658048263a2c925825e8d33",
      "is_coinbase": False,
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "scriptpubkey": "76a914e5977cf916acdba010b9d847b9682135aa3ea81a88ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 e5977cf916acdba010b9d847b9682135aa3ea81a OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "1MvyDWhroVV7BAL1twmwvY88DdvBEmPbG7",
      "value": 1100665
    }
  ]
}

# Create transaction object
tx = Tx()

# Set transaction version and locktime
tx.version = transaction_json["version"]
tx.locktime = transaction_json["locktime"]

# Add inputs
for vin in transaction_json["vin"]:
    txin = TxIn(vin["txid"], vin["vout"])
    txin.scriptSig = vin["scriptsig"]
    tx.add_input(txin)

# Add outputs
for vout in transaction_json["vout"]:
    txout = TxOut(vout["value"], Address.from_string(vout["scriptpubkey_address"]))
    txout.scriptPubKey = vout["scriptpubkey"]
    tx.add_output(txout)

# Serialize the transaction to hex
transaction_hex = tx.serialize()

print(transaction_hex)
