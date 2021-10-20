"""Module implementing encryption algorithms"""

import hashlib
import json

def hash(block: dict):
	"""Create a SHA-256 hash of a block content"""
	block_content = json.dumps(block, sort_keys = True).encode()
	return hashlib.sha256(block_content).hexdigest()


def encrypt_password(password: str):
	"""Method that takes a password and encrypts it using SHA256"""
	return hashlib.sha256(password.encode()).hexdigest()