"""Module implementing BlockChain Class"""

from block import Block
import time
import hashlib
import json	

class BlockChain:

	def __init__(self):

		self.chain = []
		self.current_transactions = []

		#create the mother block in the chain
		self.add_block(proof = 100, previous_blk_hash = '1')


	def add_block(self, proof: int, previous_blk_hash: str):
		"""Create a new block and append it to the chain"""
		new_block = Block(len(self.chain) + 1, time.time(), self.current_transactions, proof, previous_blk_hash)
		
		self.chain.append(new_block)
		
		#reset the current transactions
		self.current_transactions = []
		
		return


	def add_transaction(self, sender: str, receiver: str, data: str):
		"""Create a new transaction and add it to the list"""
		new_transaction = {
			'sender' : sender,
			'receiver' : receiver,
			'data' : data
		}
		
		self.current_transactions.append(new_transaction)
		
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

		while validate_proof(previous_proof, previous_hash, proof) == False:
			proof += 1

		return proof


	@staticmethod
	def validate_proof(previous_proof: int, previous_hash: str, proof: int):
		"""Validates the proof"""

		#f'{}{}{}' is used for string formatting in python 3
		guess = f'{previous_proof}{proof}{previous_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:3] == "000"


	@staticmethod
	def hash(block: dict):
		"""Create a SHA-256 hash of a block content"""
		block_content = json.dumps(block, sort_keys = True).encode()
		return hashlib.sha256(block_content).hexdigest()









