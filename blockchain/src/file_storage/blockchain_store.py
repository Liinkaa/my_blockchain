"""Module With the interface that the blockchain needs to work with data in json files"""

from .file_storage_config import *
from .file_store import FileStore

class BlockchainStore(FileStore):

	def __init__(self):

		super().__init__()

	def get_initial_blockchain(self):
		"""This method helps to load the blockchain in the storage when creating a new session, to keep going"""
		self.load_mined_blocks()
		return self.list_mined_blocks


	def register_mined_block(self, block_data: dict):
		"""Method to store the log data of a mined block into JSON file"""
		self.load_mined_blocks()
		self.list_mined_blocks.append(block_data)
		self.save_in_JSON(self.list_mined_blocks, JSON_FILES_PATH, BLOCKCHAIN_LOG_FILE)


	def register_transaction_booklet(self, transaction: dict):
		"""Method to store a transaction in the wallet booklet of the user"""

		#update data of the sender (check that it is not mining, the computer has no wallet)
		if transaction['sender'] != '0':

			#check that the sender has not locked his/her account
			if self.search_username(transaction['sender'])['Locked'] == False:

				self.load_transactions(transaction['sender'])
				self.list_transactions.append(transaction)
				#save in booklet
				self.save_in_JSON(self.list_transactions, WALLET_FILES_PATH, transaction['sender']+JSON_EXTENSION_FILE)
				#update his/her total currency
				self.update_wallet(transaction['sender'], -transaction['amount'])

			else:
				#cannot register transactions of a locked account
				return -1


		#receivers booklet will only be updated if he/she is registered and it is not locked
		if (not isinstance(self.search_username(transaction['receiver']), int)) and self.search_username(transaction['receiver'])['Locked'] == False:
			#update data of receiver
			self.load_transactions(transaction['receiver'])
			self.list_transactions.append(transaction)
			#save in booklet
			self.save_in_JSON(self.list_transactions, WALLET_FILES_PATH, transaction['receiver']+JSON_EXTENSION_FILE)
			#update his/her total currency
			self.update_wallet(transaction['receiver'], transaction['amount'])

		else:
			#cannot register transactions of a locked account or a not registered person
			return -1


	def register_lock_user(self, username: str):
		"""Method to encrypt wallet booklet of a user and update its status"""
		if self.check_user_lock(username) == 0:
			self.encrypt_wallet(username)
			#update 'Locked' property of a user
			self.update_lock(username, True)
		else:
			#user already locked
			return -1

	def register_unlock_user(self, username: str):
		"""Method to decrypt wallet booklet of a user and update its status"""
		if self.check_user_lock(username) == 1:
			self.decrypt_wallet(username)
			#update 'Locked' property of a user
			self.update_lock(username, False)
		else:
			#user already unlocked
			return -1
