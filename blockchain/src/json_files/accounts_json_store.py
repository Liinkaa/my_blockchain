"""Module with the interface that session needs to work with data in json files"""

from .json_storage_config import *
from .json_store import JSONStore

class AccountsJSONStore(JSONStore):

	def __init__(self):

		super().__init__()

	def register_account(self, registration: dict):
		"""Method to register a new account in JSON file"""
		self.load_accounts()

		#check if the account already exists
		if isinstance(self.search_username(registration['username']), int):

			self.list_accounts.append(registration)
			self.save_in_JSON(self.list_accounts, JSON_FILES_PATH, REGISTRATION_FILE)
			#create a corresponding wallet
			self.save_in_JSON(self.list_transactions, WALLET_FILES_PATH, registration['username']+EXTENSION_FILE)

		else:
			#if account is already registered
			return -1
		

	def look_for_account(self, username: str, password: str):
		"""Method that search for an account in the registration file.
		Return account in case of existing, otherwise -1"""

		self.load_accounts()

		for account in self.list_accounts:
			if account['username'] == username:
				if account['pass'] == password:
					return account

		#in case of not finding it
		return -1

