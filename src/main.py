"""Module with main execution program"""

from exception.blockchain_exception import BlockchainException
from user import User
from getpass import getpass

#figlet to make it more fancy
print("##################################################################################################")
print("#| |__ | | ___   ___| | _____| |__   __ _(_)_ __     ___(_)_ __ ___  _   _| | __ _| |_ ___  _ __ #")
print("#| '_ \| |/ _ \ / __| |/ / __| '_ \ / _` | | '_ \   / __| | '_ ` _ \| | | | |/ _` | __/ _ \| '__|#")	   
print("#| |_) | | (_) | (__|   | (__| | | | (_| | | | | |  \__ | | | | | | | |_| | | (_| | || (_) | |   #")
print("#|_.__/|_|\___/ \___|_|\_\___|_| |_|\__,_|_|_| |_|  |___|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|   #")
print("##################################################################################################")
print("Welcome to the Blockchain Simulator!")
print("Please type 'man' to open the user's manual\n")


#instantiate user
current_user = User()

#infinite loop
execution_loop = True
while execution_loop:

	command = input("> ")

	if command == "q":
		#exit
		execution_loop = False


	elif command == "man":
		#show the user manual
		print("\n--------------")
		print("|User's manual|")
		print("--------------")
		print("Write the following commands to perform different actions:")
		print("man -- open the manual")
		print("send_transaction -- send a peer to peer transaction")
		print("create_wallet -- get started into the blockchain and see your new keys")
		print("track_wallet -- see the total balance and transaction history of a wallet")
		print("mine -- mine the blockchain!")
		print("q -- quit\n")


	elif command == "create_wallet":
		#create a pair of keys and protect private key with given password
		try:
			print("Please, introduce a password for your private key.")
			print("It must at least contain 4 characters, an upper case letter, a lower case letter, a number and a symbol")
			password = getpass('Password: ')
			public, private = current_user.create_wallet(password)
			print("\nCongratulations! The hashes of your new keys are:\n")
			print("Hash public key: ", public)
			print("Hash private key: ", private)
			print("\nThese hashes correspond to the name of the files in which your certified keys are stored")
			print("Keep these hashes to send transactions, mine and track your wallet")

		except BlockchainException as exception:
			print(exception.message)

	elif command == "mine":
		#mine the blockchain
		try:
			wallet = str(input("Enter the hash of the wallet you want to mine with: "))
			current_user.mine(wallet)
			print("You mined a block!")

		except BlockchainException as exception:
			print(exception.message)


	elif command == "send_transaction":
		#send a transaction to another person
		sender = str(input("Enter the hash of the sender's wallet: "))
		addressee = str(input("Enter the hash of the addresse's wallet: "))			
		try:
			amount = float(input("Enter amount: "))

		except ValueError as exception:
			print("Aborted: amount must be a float")
			continue

		signature = str(input("Enter the hash of the private key: "))
		password = getpass('Enter password to unlock private key: ')
		print("Signing transaction...")
		try:
			current_user.send_transaction(sender, addressee, signature, amount, password)

			print("Sending transaction...")
			print("Receiver validating transaction...")
			print("Transaction completed successfully\n")

		except BlockchainException as exception:
			print(exception.message)

	elif command == "track_wallet":
		#show the total balance of a wallet and its transaction history
		wallet = input("Enter the hash of the wallet you want to track: ")
		transaction_history = []
		balance = 0
		try:
			transaction_history, balance = current_user.track_wallet(wallet)
			print("\nCurrent balance of the wallet: ", balance)
			print("\n\nTransaction history:\n")
			counter = 1
			for transaction in transaction_history:
				
				print("Transaction #", counter)
				print('Timestamp: ', transaction['time'])
				print('Sender:', transaction['sender'])
				print('Receiver:', transaction['receiver'])
				print('Transaction Hash: ', transaction['hash'])
				print('Amount: ', transaction['amount'])
				print("############################")
				
				counter += 1

		except BlockchainException as exception:
			print(exception.message)
	
