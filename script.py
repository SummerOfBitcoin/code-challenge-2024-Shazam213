import json
import os
import hashlib
import binascii
import bitcoinlib
from libsecp256k1 import libsecp256k1_context, SECP256K1_EC_VERIFY


def scriptpubkey_asm_to_hex(scriptpubkey_asm,script):
    scriptpubkey_hex = ""
    words = scriptpubkey_asm.split()
    if script=='p2pkh' :     
        if len(words) == 6 and words[0] == "OP_DUP" and words[1] == "OP_HASH160" and words[2]== "OP_PUSHBYTES_20" and words[4] == "OP_EQUALVERIFY" and words[5] == "OP_CHECKSIG":
            scriptpubkey_hex = "76a014" + words[3]+ "88ac"
    elif script=='v0_p2wsh' :
        if len(words) == 3 and words[0] == "OP_0" and words[1] == "OP_PUSHBYTES_32":
            scriptpubkey_hex = "0020" + words[2]
    elif script == 'p2sh':
        if len(words) == 4 and words[0] == "OP_HASH160" and words[1] == "OP_PUSHBYTES_20" and words[3]=="OP_EQUAL":
            scriptpubkey_hex= "a914"+words[2]+"87"
    elif script=='v0_p2wpkh':
        if len(words) == 3 and words[0] == "OP_0" and words[1] == "OP_PUSHBYTES_20":
            scriptpubkey_hex = "0014" + words[2]
    elif script== 'v1_p2tr':
        if len(words) == 3 and words[0] == "OP_PUSHNUM_1" and words[1] == "OP_PUSHBYTES_32":
            scriptpubkey_hex = "5120" + words[2]
        
    
    return scriptpubkey_hex

def op_hash160(data):
  
  # SHA-256 hash
  sha256_hash = hashlib.sha256(data).digest()
  # RIPEMD-160 hash
  ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
  return ripemd160_hash.hex()


def validate_p2tr():
def validate_p2pkh(dict):
    signature = dict["scriptsig_asm"].split(" ")[1]
    pub_key= dict["scriptsig_asm"].split(" ")[3]
    pub_key_hash = op_hash160(pub_key)
    bitcoin_add= dict["prevout"]["scriptpubkey_asm"].split(" ")[3]
    if(pub_key_hash != bitcoin_add): return False

 
def validate_p2wsh():
def validate_p2sh():
def validate_p2wpkh():
   


#validate transaction og
def validate_transaction(transaction):

    vin_value=0
    vout_value=0
    for dict in transaction['vin']:
        vin_value=vin_value+dict['prevout']['value']
        script= dict['prevout']['scriptpubkey_type']
        scriptpubkey_hex = scriptpubkey_asm_to_hex(dict['prevout']['scriptpubkey_asm'],script)
        if scriptpubkey_hex == dict['prevout']['scriptpubkey']: 
            if script == 'v1_p2tr':   
                validate_p2tr()
            elif script == 'p2pkh':
                validate_p2pkh(dict)
            elif script== 'v0_p2wsh':
                validate_p2wsh()
            elif script== 'p2sh':
                validate_p2sh()
            elif script== 'v0_p2wpkh':
                validate_p2wpkh()
            
    
    for dict in transaction['vout']:
        vout_value=vout_value+dict['value']
    transaction_fees= vin_value-vout_value
    






## main function
mempool_folder = "mempool"
transactions = []
for filename in os.listdir(mempool_folder):
    if filename.endswith(".json"):
        with open(os.path.join(mempool_folder, filename)) as file:
            transaction_data = json.load(file)
            transactions.append(transaction_data)

for idx,tx in enumerate(transactions):
    print(idx)
    validate_transaction(tx)


