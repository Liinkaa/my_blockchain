"""This module implements all the actions that a user can take"""

import re
from blockchain import BlockChain
from exception.blockchain_exception import BlockchainException
from encryption import hash_dict

class User(BlockChain):
	"""Class that defines the user interface"""

	def __init__(self):
		"""inherit all methods from parent class"""
		super().__init__()

	def __password_robustness(self, password: str):
		"""Method that checks if a password is has upppercase characters, symbols and numbers"""
		how_robust = 0

		if len(password) >= 4:
			how_robust += 1

		#upper case letters
		find_upper = re.findall('[A-Z]', password)
		if find_upper:
			how_robust +=1

		#numbers
		find_numbers = re.findall('[0-9]+', password)
		if find_numbers:
			how_robust +=1

		#symbols
		find_symbols = re.findall('[^A-Za-z0-9]', password)
		if find_symbols:
			how_robust +=1

		if how_robust != 4:
			return -1
		else:
			return 0


	def create_wallet(self, password: str):
		"""Method to create pair of keys and wallet"""

		if self.__password_robustness(password) == -1:
			raise BlockchainException("Password is too weak")

		#create public and private keys
		keys = self.create_keys(password)
		
		if isinstance(keys, int):
			raise BlockchainException("Password must be from 4 to 1023 characters")
	
		return keys[0], keys[1]

	
	def mine(self, wallet: str):
		"""Method to mine blocks and generate coins in a blockchain"""

		#Check that wallet exists, it is in correct format and user is not trying to mine as the root
		if isinstance(self.search_public_key(wallet), int) or wallet == "root":
			raise BlockchainException("Invalid wallet format or not found")
		
		#run proof algorithm to get next proof
		new_proof = self.proof_of_work(self.last_block)

		#now forge the new block and add it to the chain
		self.add_block(new_proof, hash_dict(self.last_block), wallet)
		

	def send_transaction(self, sender: str, receiver: str, signature: str, amount: float, password: str):
		"""Method to emulate sending a transaction between two wallets through the blockchain"""

		#Check that wallet exists, it is in correct format and user is not trying to send a transaction to/as the root
		if (isinstance(self.search_public_key(sender), int)
		 or isinstance(self.search_public_key(receiver), int)
		  or receiver == "root" or sender == 'root'):

			raise BlockchainException("\nInvalid wallet format or not found")

		#Check that nobody is sending money to his/herself
		if sender == receiver:
			raise BlockchainException("\nSender and receiver of the transaction must be different")

		#Check if input amount is negative or 0
		if amount <= 0:
			raise BlockchainException("Amount must be bigger than 0")

		#Check if sender is sending more than his/her available resources
		if amount > self.track_wallet(sender)[1]:
			raise BlockchainException("Not enough currency available")

		#Check if transaction was sent succesfully
		return_value = self.p2p_transaction(sender, receiver, signature, amount, password)
		if return_value == -1:
			raise BlockchainException("Sender or receiver is not verified")
		elif return_value == -2:
			raise BlockchainException("Unable to sign transaction")
		elif return_value == -3:
			raise BlockchainException("Receiver could not validate transaction")


	def track_wallet(self, wallet: str):
		"""Method that allows the user to check the balance of any given wallet and
		transaction history in the blockchain"""

		#Check that wallet exists and it is in correct format
		if isinstance(self.search_public_key(wallet), int):
			raise BlockchainException("Wallet not found")

		#return a list with all transactions and computed balance
		booklet, balance = self.wallet_transactions(wallet)
		return booklet, balance


