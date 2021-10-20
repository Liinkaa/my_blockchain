"""Module that implements the actions that the user can take"""

from json_files.accounts_json_store import AccountsJSONStore
from blockchain import BlockChain
from exception.account_management_exception import AccountManagementException

class SessionManagement(AccountsJSONStore):
	"""Class to encapsulate methods and actions taken in a session by a user
	This class extends JSONStore"""

	def __init__(self):
		#get all the methods from the parent class
		super().__init__()


	def register(self, username: str, password: str):
		"""Method to get registered in the DB"""
		new_user = {

			'username': username,
			'pass': password,
			'wallet': 0

		}
		#save in json file
		if isinstance(self.register_account(new_user), int):
			raise AccountManagementException("User already registered")


	def login(self, username: str, password: str):
		"""Method to check if input account credentials are correct"""
		if not isinstance(self.look_for_account(username, password), dict):
			#if credentials are wrong
			raise AccountManagementException("Wrong credentials")

		else:
			return username

	def man(self):
		"""Method to print manual of the possible actions that the user can do"""
		print("--------------")
		print("|User's manual|")
		print("--------------")
		print("Write the following commands to perform different actions:")
		print("man -- open the manual                   |  register -- create an account")
		print("login -- login with an existent account  |  q -- quit\n")

