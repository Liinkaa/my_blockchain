"""This module implements all the actions that a logged in user can take"""

from blockchain import BlockChain
from encryption import *

class User(BlockChain):
	"""Class that encapsulates all methods that a user can use
	This class extends BlockChain"""

	def __init__(self, username):
		#get all the methods from the parent class
		super().__init__()
		#store the name of the user using the blockchain
		self.username = username

	def mine(self):
		"""Method to mine blocks and generate coins in a blockchain"""
		#run proof algorithm to get next proof
		new_proof = self.proof_of_work(self.last_block)

		#if a new proof is found, give a reward
		#0 is the sender to represent the machine as a sender
		self.add_transaction('0', self.username, 1)

		#now forge the new block and add it to the chain
		added_block = self.add_block(new_proof, hash(self.last_block))
		

	def send_transaction(self, receiver: str, amount: int):
		"""Method to send a transaction
		The sender is always the person logged in as a user"""
		self.add_transaction(self.username, receiver, amount)

	def man(self):
		"""Method to print manual of the possible actions that the user can do"""
		print("--------------")
		print("|User's manual|")
		print("--------------")
		print("Write the following commands to perform different actions:")
		print("man -- open the manual                   			   |  mine -- mine the blockchain!")
		print("send_transaction -- send a transaction to another user  |  q -- quit\n")

