"""Module implementing encryption algorithms"""

import hashlib
import json
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

################## HASH ENCRYPTION FUNCTIONS ##################

def hash(block: dict):
	"""Create a SHA-256 hash of a block content"""
	block_content = json.dumps(block, sort_keys = True).encode()
	return hashlib.sha256(block_content).hexdigest()


def encrypt_password(password: str):
	"""Method that takes a password and encrypts it using SHA256"""
	return hashlib.sha256(password.encode()).hexdigest()


################## SYMMETRIC ENCRYPTION FUNCTIONS ##################

def generate_symmetric_key(randomness: int):
    """Method that generates a random key"""
    return get_random_bytes(randomness)


def symmetric_encryption(data: bytes):
    """Method that encrypts input data (bytes) using AES128"""
    #generate a random key
    key = generate_symmetric_key(16) #16 bytes = 128 bits key for AES

    #create a cipher
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    #obtain encrypted message as bytes and Authentication MAC tag for a message
    ciphertext, tag = cipher.encrypt_and_digest(data)

    #return a list with the important data of the symmetric encryption
    return_list = [ciphertext, key, tag, nonce]

    return return_list


def symmetric_decryption(data: bytes, key: bytes, tag: bytes, nonce: bytes):
    """Method that decrypts an AES encyrpted message"""
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    plaintext = cipher.decrypt(data)

    try:
        cipher.verify(tag)
        #return decrypted message
        return plaintext
    except ValueError:
        #Key incorrect or message corrupted
        return -1

#not used?
def encode(binary_data: bytes):
    """Method that encodes input data (bytes) into base 64"""
    return base64.b64encode(binary_data)


