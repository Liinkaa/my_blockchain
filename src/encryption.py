"""Module implementing encryption algorithms"""

import json
import hashlib
import base64
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


################## HASH ENCRYPTION FUNCTIONS ##################

def hash_dict(block: dict):
	"""USED IN BLOCKCHAIN Create a SHA-256 hash of a block content"""

	block_content = json.dumps(block, sort_keys = True).encode()
	return hashlib.sha256(block_content).hexdigest()


def hash_str(text: str):
	"""Method that takes a string and encrypts it using SHA256"""

	return hashlib.sha256(text.encode()).hexdigest()


def encode(binary_data: bytes):
    """Method that encodes input data (bytes) into base 64"""

    return base64.b64encode(binary_data)


################## ASYMMETRIC ENCRYPTION FUNCTIONS ##################
    
def sign(message: bytes, private_key: str, password: str):
    """Method that signs an input message using a private key"""
    
    key = ECC.import_key(private_key, passphrase = password)
    hasher = SHA256.new(message)
    signer =DSS.new(key, 'fips-186-3')
    signature = signer.sign(hasher)
    return signature


def confirm_authenticity(message: bytes, signature: bytes, public_key: bytes):
    """Method that decrypts a signed message with the public key of the 
    person who signed it to check authenticity of the message"""
    
    key = ECC.import_key(public_key)
    hasher = SHA256.new(message)
    verifier = DSS.new(key, 'fips-186-3')
    verifier.verify(hasher, signature)


