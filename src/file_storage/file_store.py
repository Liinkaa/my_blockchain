"""Module that implementing file storage class methods"""

import json
import os
from .file_store_config import *
from encryption import hash_str

class FileStore:
	"""Class to encapsulate all methods treating file management"""

	def __init__(self):

		#buffer to load a blockchain from storage
		self.__list_mined_blocks = [] 

	################## GENERAL STORAGE METHOD ################## 

	def __save_in_JSON(self, data: list, path: str, filename: str):
		"""Save contents of data in JSON file given by filename"""

		with open(path+filename, 'w') as outfile:
			json.dump(data, outfile, indent = 2)


	################## INTERFACE FOR BLOCKCHAIN ################## 
	
	def get_current_blockchain(self):
		"""This method helps to load the blockchain in the storage when creating a new session, to keep going"""

		#give permissions of execution in case it is the first time exeucting
		file = os.popen(GIVE_PERMISSIONS + ' ' + CA_SCRIPT_FILE + ' ' + CREATE_KEYS_CA_FILE + ' ' + CHANGE_NAMES_FILE)
		file.close()

		with open(BLOCKCHAIN_STORAGE_PATH+BLOCKCHAIN_LOG_FILE, 'r') as openfile:
			self.__list_mined_blocks = json.load(openfile)
		return self.__list_mined_blocks


	def generate_certificates(self):
		"""Method that generates certificate authorities"""

		file = os.popen(EXECUTE + CA_SCRIPT_FILE)
		file.close()


	def generate_keys(self, password: str):
		"""Method that generates a pair of certified keys"""

		#create keys
		f = os.popen(EXECUTE + CREATE_KEYS_CA_FILE+' '+password)
		f.close()

		#obtain public and private keys to hash them
		try:
			public = open(LOCAL_HOST_PUBLIC + PUBLIC_KEY_FILE_AUX + KEY_FILE_EXTENSION).read()
			public_hash = hash_str(public)

			private = open(LOCAL_HOST_PRIVATE + KEY_FILE_AUX + KEY_FILE_EXTENSION).read()
			private_hash = hash_str(private)
		
		except FileNotFoundError:
			return -1
		
		#change names to hashes
		f = os.popen(EXECUTE + CHANGE_NAMES_FILE + ' ' + public_hash + ' ' + private_hash)
		f.close()

		return public_hash, private_hash


	def get_root_signature(self):
		"""Method that loads the private key of the root, used to sign the reward transactions
		given to miners"""

		key_str = open(ROOT_FOLDER_PATH+ROOT_KEY+KEY_FILE_EXTENSION).read()
		return key_str


	def register_mined_block(self, block_data: dict):
		"""Method to store the log data of a mined block into JSON file"""

		self.get_current_blockchain()
		self.__list_mined_blocks.append(block_data)
		self.__save_in_JSON(self.__list_mined_blocks, BLOCKCHAIN_STORAGE_PATH, BLOCKCHAIN_LOG_FILE)


	def get_public_key(self, hash_public_k: str):
		"""Method that receives the hash of a public key (name of the file) and returns its string
		representation in case it exists"""

		try:
			key_str = open(PUBLIC_KEYS_FOLDER_PATH+hash_public_k+KEY_FILE_EXTENSION, 'r').read()
			return key_str
		except FileNotFoundError:
			return -1


	def get_private_key(self, hash_private_k: str):
		"""Method that receives the hash of a private key (name of the file) and returns its string
		representation in case it exists"""

		try:
			key_str = open(LOCAL_HOST_PRIVATE+hash_private_k+KEY_FILE_EXTENSION, 'r').read()
			return key_str
		except FileNotFoundError:
			return -1


	def check_certification(self, hash_public_k: str):
		"""Method that receives the hash of a public key (name of the file) and returns 
		if the wallet is certified or not"""
		
		try:
			open(CERTIFICATES_FOLDER_PATH + hash_public_k + CERTIFICATE_FILE_EXTENSION)
		except FileNotFoundError:
			return -1

