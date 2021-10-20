"""Module implementing BlockChain Class"""

import time
from encryption import *
from block import Block
from json_files.blockchain_json_store import BlockchainJSONStore

class BlockChain(BlockchainJSONStore):

	def __init__(self):

		super().__init__()

		self.chain = [] 
		self.current_transactions = []

		#Load what is saved in storage
		self.__initialize_blockchain()


	def __initialize_blockchain(self):
		"""Method that helps to transform dictionaries from json file into blocks from the stored log"""
		#reset the chain to make sure
		self.chain = []
		storage =self.get_initial_blockchain()
		#create the mother block in the chain in case it is empty
		if len(storage) == 0:
			self.add_block(proof = 100, previous_blk_hash = '1')
			return
		else:
			for json_block in storage:
				self.chain.append(Block(json_block['index'], json_block['timestamp'], json_block['transactions'], json_block['proof'], json_block['previous_blk']))

	def add_block(self, proof: int, previous_blk_hash: str):
		"""Create a new block and append it to the chain"""
		new_block = Block(len(self.chain) + 1, time.time(), self.current_transactions, proof, previous_blk_hash)
		
		self.chain.append(new_block)
		
		#reset the current transactions
		self.current_transactions = []

		#register this data in a the mining log
		self.register_mined_block(new_block.content)

		return new_block


	def add_transaction(self, sender: str, receiver: str, amount: int):
		"""Create a new transaction and add it to the list"""
		new_transaction = {
			'sender' : sender,
			'receiver' : receiver,
			'amount' : amount
		}
		
		self.current_transactions.append(new_transaction)
		
		#register this transaction in the log files
		self.register_transaction_booklet(new_transaction)

		#return the index of the block that will hold this transaction
		return self.last_block['index'] + 1


	@property
	def last_block(self):
		"""Return the content dictionary of the last block in the chain"""
		return self.chain[-1].content


	def proof_of_work(self, end_block: dict):
		"""It is how new blocks are created (or mined). 
		Finds a number x such that hash(px) contains 3 leading zeroes
		Where p is the previous proof and x is the new proof"""
		previous_proof = end_block['proof']
		previous_hash = hash(end_block)

		#initialize guess to 0
		proof = 0

		while self.validate_proof(previous_proof, previous_hash, proof) == False:
			proof += 1

		return proof


	@staticmethod
	def validate_proof(previous_proof: int, previous_hash: str, proof: int):
		"""Validates the proof"""

		#f'{}{}{}' is used for string formatting in python 3
		guess = f'{previous_proof}{proof}{previous_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:3] == "000"










