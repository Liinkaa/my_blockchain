"""Module that implements all methods to treat json files"""

import json
from .json_storage_config import *

class JSONStore:
	"""This class is used to treat json files.
	Methods should not be visible to the user"""

	def __init__(self):

		#initialize necessary buffers for reading and writing from JSON files
		self.list_accounts = []
		self.list_mined_blocks = []
		self.list_transactions = []

	################## GENERAL JSON METHODS ################## 

	def save_in_JSON(self, data: list, path: str, filename: str):
		"""Save contents of data in JSON file given by filename"""
		with open(path+filename, 'w') as outfile:
			json.dump(data, outfile, indent = 2)


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

		with open(WALLET_FILES_PATH+username+EXTENSION_FILE, 'r') as openfile:
			self.list_transactions = json.load(openfile)


	def update_wallet(self, username: str, amount: int):
		"""Method to update the total money a user has
		This method supposes that the person is registered"""
		self.load_accounts()
		#find the corresponding person to update his/her data
		for account in self.list_accounts:
			if account['username'] == username:
				account['wallet'] += amount

		#save updated version
		self.save_in_JSON(self.list_accounts, JSON_FILES_PATH, REGISTRATION_FILE)


	"""
	def reset_json_file(self):
		#Method to remove everything from the registrations json file
		#THIS METHOD IS ONLY USED FOR TESTING
		self.load_accounts()
		for account in self.list_accounts:
			self.list_accounts.remove(account)

		self.save_in_JSON(self.list_accounts, JSON_FILES_PATH, REGISTRATION_FILE)
	"""

