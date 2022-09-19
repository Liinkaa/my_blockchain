"""Module implementing the BlockChain"""

import time
from encryption import *
from block import Block
from file_storage.file_store import FileStore

class BlockChain(FileStore):

	def __init__(self):
		"""Inherit all public methods from FileStore"""
		super().__init__()

		#buffer for the current chain
		self.chain = [] 
		#buffer for the current transactions
		self.current_transactions = []
		#Load what is saved in storage
		self.__initialize_blockchain()


	def __initialize_blockchain(self):
		"""Method that loads the current state of the blockchain in storage"""

		storage = self.get_current_blockchain()

		#in case the blockchain is new
		if len(storage) == 0:
			
			#create root keys and certification authoritiess
			self.generate_certificates()

			#add an initial transaction (from the root to itself)
			self.add_transaction({'time': time.time(), 'hash': 'root-transaction', 'signature': 'root', 'sender': 'root', 'receiver': 'root', 'amount': 0.0})

			#add the first root block to the chain
			self.add_block(proof = 100, previous_blk_hash = 'root', reward_wallet = 'root')

		else:

			#load what is saved in storage	
			for json_block in storage:
				self.chain.append(Block(json_block['index'], json_block['timestamp'], json_block['transactions'], json_block['proof'], json_block['previous_blk']))

		
	def __sender_sign_transaction(self, sender: str, receiver: str, signature: str, amount: float, password: str):
		"""Method that creates the transaction to be sent and signed with the sender's private key"""

		#see if both sender and receiver are certified users
		if isinstance(self.check_certification(sender), int) or isinstance(self.check_certification(receiver), int):
			return -1

		#create the new hash using the previous last transaction and the receivers public key
		to_be_signed = str(self.last_block['transactions'][-1])+receiver
		transaction_hash = hash_str(to_be_signed)

		try:
			#the sender signs the transaction
			signature = sign(bytes(transaction_hash, 'utf-8'), self.get_private_key(signature), password) 
		except ValueError:
			return -2

		#instantiate transaction
		new_transaction = {

			'time' : time.time(),
			'hash' : transaction_hash,
			'signature' : str(signature)[2:-1], #avoid byte b'' decorator to prevent JSON file errors
			'sender' : sender, 
			'receiver' : receiver, 
			'amount' : amount 
			
		}

		#correct execution
		return new_transaction


	def __receiver_validate_transaction(self, transaction: dict):
		"""Method that emulates the reception of a transaction. It must be verified
		by the receiver using the sender's private key"""

		try:
			#check the authenticity of the transaction
			#confirm_authenticity(message, signature, public_key)
			confirm_authenticity(bytes(transaction['hash'], 'utf-8'), bytes(transaction['signature'], 'utf-8').decode('unicode-escape').encode('ISO-8859-1'), self.get_public_key(transaction['sender']))
		except ValueError as exception:
			#in case the transaction could not be verified
			return -1


	def p2p_transaction(self, sender: str, receiver: str, signature: str, amount: float, password: str):
		"""Method to emulate a peer to peer transaction using the blockchain infrastructure"""

		#sender sends signed transaction
		signed_transaction = self.__sender_sign_transaction(sender, receiver, signature, amount, password)

		#if transaction has not been signed succesfully
		if isinstance(signed_transaction, int):
			if signed_transaction == -1:
				#sender or receiver are not verified
				return -1
			#could not sign the transaction
			return -2

		#receiver receives transaction and checks authentication with sender's public key
		if isinstance(self.__receiver_validate_transaction(signed_transaction), int):
			#receiver could not validate transaction
			return -3

		#if transaction was succesfully authenticated
		self.add_transaction(signed_transaction)
		#correct execution
		return 0


	def add_transaction(self, transaction: dict):
		"""Add a new transaction to the block to be mined"""

		self.current_transactions.append(transaction)


	def add_block(self, proof: int, previous_blk_hash: str, reward_wallet: str):
		"""Create a new block and append it to the chain and reward the miner who mined the block"""

		new_block = Block(len(self.chain) + 1, time.time(), self.current_transactions, proof, previous_blk_hash)
		
		#avoid rewarding the root when it is initializing itself
		if reward_wallet != 'root':
			#miner is rewarded 1 coin and transaction is signed by the root

			to_be_signed = str(self.last_block['transactions'][-1])+reward_wallet
			transaction_hash = hash_str(to_be_signed)
			reward = {
				'time': time.time(), 
				'hash': transaction_hash, 
				'signature': str(self.get_root_signature())[28:-27],
				'sender': 'root', 
				'receiver': reward_wallet, 
				'amount': 1.0
				}

			self.add_transaction(reward)

		#add new block to the chain
		self.chain.append(new_block)

		#reset the current transactions
		self.current_transactions = []

		#register this data in a the mining log
		self.register_mined_block(new_block.content)
		

	@property
	def last_block(self):
		"""Return the content dictionary of the last block in the chain"""

		return self.chain[-1].content


	def proof_of_work(self, end_block: dict):
		"""It is how new blocks are created (or mined). 
		Finds a number x such that hash(px) contains 3 leading zeroes
		Where p is the previous proof and x is the new proof"""

		previous_proof = end_block['proof']
		previous_hash = hash_dict(end_block)

		#initialize guess to 0
		proof = 0

		#try guessing
		while self.validate_proof(previous_proof, previous_hash, proof) == False:
			proof += 1

		#found a guess
		return proof


	@staticmethod
	def validate_proof(previous_proof: int, previous_hash: str, proof: int):
		"""Validates the proof"""

		#f'{}{}{}' is used for string formatting in python 3
		guess = f'{previous_proof}{proof}{previous_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:3] == "000"


	def wallet_transactions(self, wallet: str):
		"""Method that returns the total balance of a wallet and the list of transactions
		in which the input wallet is involved"""

		booklet = []
		balance = 0.0

		for block in self.chain:
			for transaction in block.content['transactions']:
				if transaction['sender'] == wallet:
					
					balance -= transaction['amount']
					booklet.append(transaction)

				elif transaction['receiver'] == wallet:
					
					balance += transaction['amount']
					booklet.append(transaction)

		return booklet, balance


	def create_keys(self, password: str):
		"""Method to create the RSA public and private keys using elliptic curves and store them"""

		return self.generate_keys(password)


	def search_public_key(self, target: str):
		"""Method that receives the hash of the public key, loads it from local 
		storage and returns it as a string"""

		return self.get_public_key(target)


