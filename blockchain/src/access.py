"""Module that implements account creation and management"""

from json_store import JSONStore
from encryption import *


class AccountManagement(JSONStore):
	"""This class extends JSONStore"""

	def register(self, username: str, password: str):
		"""Method to get registered in the DB"""
		new_user = {

			'username': username,
			'pass': encrypt_password(password)

		}
		#save in json file
		self.register_account(new_user)

	"""
	def delete_account(self, username: str, password: str):
		#Method to remove an account

		if(self.remove_account(username, password) < 0):
			#print("Account not found in the DB\n")
			return -1
	"""

	def access(self, username: str, password: str):
		"""Method to check if input account credentials are correct"""
		if(self.look_for_account(username, password) <0):
			return -1

		



