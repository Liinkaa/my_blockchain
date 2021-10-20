"""Defining the class Block"""

class Block:

	def __init__(self, index: int, timestamp: float, transactions: list, proof: int, previous_blk_hash = None):
		"""Each block in the block chain needs to be initialized with a timestamp, 
		the transaction data and the hash of the previous block"""
		self.__content = {

			'index' : index,
			'timestamp' : timestamp,
			'transactions' : transactions,
			'proof' : proof,
			'previous_blk' : previous_blk_hash #hash of the previous block

		}
		
	@property
	def content(self):
		"""Property method to see the content of a block"""
		return self.__content
	