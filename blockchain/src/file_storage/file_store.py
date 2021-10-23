"""Module that implements all methods to treat json files"""

import json
import os
from .file_storage_config import *
from .encryption import *

class FileStore:
	"""This class is used to treat json files.
	Methods should not be visible to the user"""

	def __init__(self):

		#initialize necessary buffers for reading and writing from JSON files
		self.list_accounts = []
		self.list_mined_blocks = []
		self.list_transactions = []
		self.list_wallet = []

	################## GENERAL STORAGE METHODS ################## 

	def save_in_JSON(self, data: list, path: str, filename: str):
		"""Save contents of data in JSON file given by filename"""
		with open(path+filename, 'w') as outfile:
			json.dump(data, outfile, indent = 2)

	
	def save_in_generic_file(self, data: str, path: str, filename: str):
		"""Save data into a file"""
		file = open(path+filename, 'w')
		file.write(data)
		file.close()


	def create_folder(self, directory: str):
		"""Method to create folders"""
		try:
			os.mkdir(directory)
		#in case the folder already exists
		except OSError as error:
			pass


	################## METHODS FOR ACCOUNT MANAGEMENT ################## 

	def load_accounts(self):
		"""Method to initialize data of registered people"""
		with open(JSON_FILES_PATH+REGISTRATION_FILE, 'r') as openfile:
			self.list_accounts = json.load(openfile)


	def search_username(self, username: str):
		"""Method that search for a username account in the registration file.
		This will be used to check if a user is already registered"""
		self.load_accounts()
		for account in self.list_accounts:
			if account['username'] == username:
				return account

		#in case of not finding it
		return -1


	################## METHODS FOR BLOCKCHAIN ################## 

	def load_mined_blocks(self):
		"""Method to initialize data of mined blocks the blockchain"""
		with open(JSON_FILES_PATH+BLOCKCHAIN_LOG_FILE, 'r') as openfile:
			self.list_mined_blocks = json.load(openfile)


	def load_transactions(self, username: str):
		"""Method to initialize transactions of a user"""
		with open(WALLET_FILES_PATH+username+JSON_EXTENSION_FILE, 'r') as openfile:
			self.list_transactions = json.load(openfile)


	def load_wallet(self, username: str):
		"""Method to initialize data of a wallet"""
		with open(WALLET_FILES_PATH+username+JSON_EXTENSION_FILE, 'r') as openfile:
			self.list_wallet = json.load(openfile)


	def update_wallet(self, username: str, amount: int):
		"""Method to update the total money a user has
		This method supposes that the person is registered"""
		self.load_wallet(username)
		#update his/her balance
		self.list_wallet[0]['Balance'] += amount
		#save updated version
		self.save_in_JSON(self.list_wallet, WALLET_FILES_PATH, username+JSON_EXTENSION_FILE)


	################## METHODS FOR SYMMETRIC ENCRYPTION ################## 

	def encrypt_wallet(self, username: str):
		"""Method that encrypts the wallet of a user, using his/her password as a key"""

		#look for that wallet
		self.load_wallet(username)

		#convert json data into str
		wallet_data = str(self.list_wallet)

		#convert string into bytes
		wallet_data_bytes = bytes(wallet_data, 'utf-8')

		#encrypt the data
		encryption_result = symmetric_encryption(wallet_data_bytes)
		#save data
		self.save_in_generic_file(self.string_no_byte_decorator(encryption_result[0]), WALLET_FILES_PATH, username)
		self.save_keys(username, encryption_result[1], encryption_result[2], encryption_result[3])


		#delete wallet json file
		os.remove(WALLET_FILES_PATH+username+JSON_EXTENSION_FILE)


	def decrypt_wallet(self, username: str):
		"""Method that decrypts the wallet of a user"""

		#open encrypted wallet
		encrypted_wallet_data = self.encode_and_fix(WALLET_FILES_PATH+username)
		#open key file
		key_data = self.encode_and_fix(ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION+KEY_FILE_NAME)
		#open extra data (MAC tag)
		extra_data = self.encode_and_fix(ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION+EXTRA_FILE_NAME)
		#open nonce for cipher
		nonce_data = self.encode_and_fix(ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION+NONCE_FILE_NAME)

		#use decryption algorithm
		plain_text = symmetric_decryption(encrypted_wallet_data, key_data, extra_data, nonce_data)
		
		#save data into json file
		self.list_wallet = []
		self.list_wallet = list(eval(self.string_no_byte_decorator(plain_text)))
		self.save_in_JSON(self.list_wallet, WALLET_FILES_PATH, username+JSON_EXTENSION_FILE)

		#remove encrypted files
		self.remove_encryption_files(username)


	def encode_and_fix(self, filepath: str):
		"""Method that encodes the content of a file and corrects the double backlash error that happens"""
		file_object = open(filepath)
		file_data = bytes(file_object.read(), 'utf-8')
		file_data_fix = file_data.decode('unicode-escape').encode('ISO-8859-1')

		return file_data_fix


	def string_no_byte_decorator(self, data: bytes):
		"""Method that converts bytes to string and neglects the b'...' clause"""
		return str(data)[2:-1]


	def remove_encryption_files(self, username: str):
		"""Method that removes the associated encryption files of a user after decrypting"""
		os.remove(WALLET_FILES_PATH+username)
		os.remove(ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION+KEY_FILE_NAME)
		os.remove(ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION+EXTRA_FILE_NAME)
		os.remove(ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION+NONCE_FILE_NAME)


	def save_keys(self, username:str, key: bytes, extra: bytes, nonce: bytes):
		"""Method that saved encryption data into files. Input key and extra are bytes"""
		#open a directory for the user
		directory = ENCRYPTION_FOLDER_PATH+username+DIRECTORY_EXTENSION
		self.create_folder(directory)

		#save data
		self.save_in_generic_file(self.string_no_byte_decorator(key), directory, KEY_FILE_NAME)
		self.save_in_generic_file(self.string_no_byte_decorator(extra), directory, EXTRA_FILE_NAME)
		self.save_in_generic_file(self.string_no_byte_decorator(nonce), directory, NONCE_FILE_NAME)


	def update_lock(self, username: str, status: bool):
		"""Method that updates the 'Locked' condition of a user"""
		self.load_accounts()
		for index in range(len(self.list_accounts)):
			if self.list_accounts[index]['username'] == username:
				self.list_accounts[index]['Locked'] = status

		self.save_in_JSON(self.list_accounts, JSON_FILES_PATH, REGISTRATION_FILE)


	def check_user_lock(self, username: str):
		"""Method that checks if a user is already locked"""
		self.load_accounts()
		for index in range(len(self.list_accounts)):
			if self.list_accounts[index]['username'] == username:
				if self.list_accounts[index]['Locked'] == True:
					return 1
		#if it is not locked
		return 0

