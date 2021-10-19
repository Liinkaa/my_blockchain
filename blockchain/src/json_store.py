"""Module for JSON file management"""

import json
from pathlib import Path
from encryption import *

JSON_FILES_PATH = str(Path.home()) + "/Desktop/blockchain/storage/"
REGISTRATION_FILE = "credentialsStore.json"

class JSONStore:

	def __init__(self):

		self._list_accounts = []
		self.load_accounts()


	def load_accounts(self):
		"""Method to initialize data of registered people"""
		with open(JSON_FILES_PATH+REGISTRATION_FILE, 'r') as openfile:
			self._list_accounts = json.load(openfile)
			#print(self._list_accounts)
			#print(type(self._list_accounts))


	def register_account(self, registration: dict):
		"""Method to register a new account in JSON file"""
		self.load_accounts()
		self._list_accounts.append(registration)
		self.save_in_JSON(self._list_accounts, REGISTRATION_FILE)
		

	def look_for_account(self, username: str, password: str):
		"""Method that search for an account in the registration file.
		Return account in case of existing, otherwise -1"""

		self.load_accounts()

		for account in self._list_accounts:
			if account['username'] == username:
				if account['password'] == encrypt_password(password):
					return account

		#in case of not finding it
		return -1


	def remove_account(self, username: str, password: str):
		"""Method to remove an account from the registration file"""
		account = self.look_for_account(username, password)
		if(account<0):
			#error: not found
			return -1

		#if found remove it from the list
		self._list_accounts.remove(account)
		#update json file
		self.save_in_JSON(self._list_accounts, REGISTRATION_FILE)


	def save_in_JSON(self, data: list, filename: str):
		"""Save contents of data in JSON file given by filename"""
		with open(JSON_FILES_PATH+filename, 'w') as outfile:
			json.dump(data, outfile, indent = 2)

