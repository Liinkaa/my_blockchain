"""Module With the interface that the blockchain needs to work with data in json files"""

from .json_storage_config import *
from .json_store import JSONStore

class BlockchainJSONStore(JSONStore):

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
			self.load_transactions(transaction['sender'])
			self.list_transactions.append(transaction)
			#save in booklet
			self.save_in_JSON(self.list_transactions, WALLET_FILES_PATH, transaction['sender']+EXTENSION_FILE)
			#update his/her total currency
			self.update_wallet(transaction['sender'], -transaction['amount'])


		#receivers booklet will only be updated if he/she is registered
		if not isinstance(self.search_username(transaction['receiver']), int):
			#update data of receiver
			self.load_transactions(transaction['receiver'])
			self.list_transactions.append(transaction)
			#save in booklet
			self.save_in_JSON(self.list_transactions, WALLET_FILES_PATH, transaction['receiver']+EXTENSION_FILE)
			#update his/her total currency
			self.update_wallet(transaction['receiver'], transaction['amount'])

