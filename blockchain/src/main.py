"""Module with main execution program"""

from exception.account_management_exception import AccountManagementException
from session import SessionManagement
from user import User
from blockchain import BlockChain

#figlet to make it more fancy
print("##################################################################################################")
print("#| |__ | | ___   ___| | _____| |__   __ _(_)_ __     ___(_)_ __ ___  _   _| | __ _| |_ ___  _ __ #")
print("#| '_ \| |/ _ \ / __| |/ / __| '_ \ / _` | | '_ \   / __| | '_ ` _ \| | | | |/ _` | __/ _ \| '__|#")	   
print("#| |_) | | (_) | (__|   | (__| | | | (_| | | | | |  \__ | | | | | | | |_| | | (_| | || (_) | |   #")
print("#|_.__/|_|\___/ \___|_|\_\___|_| |_|\__,_|_|_| |_|  |___|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|   #")
print("##################################################################################################")
print("Welcome to the Blockchain Simulator!")
print("Please type 'man' to open the user's manual\n")

#Instantiate account management for the session
session = SessionManagement()

#infinite loop
login_loop = True
while login_loop:

	command = input("> ")

	if command == "q":
		#end loop
		login_loop = False

	elif command == "man":
		#show manual
		session.man()

	elif command == "register":
		#register account
		username = input("Please enter a username: ")
		password = input("Please enter password: ")

		try:
			session.register(username, password)

		except AccountManagementException as exception:
			print(exception.message)


	elif command == "login":
		#login
		username = input("Enter a username: ")
		password = input("Enter password: ")

		try:
			valid_user = session.login(username, password)
			print("Successfully logged in :)\n")
			login_loop = False


		except AccountManagementException as exception:
			print(exception.message)

#instantiate user
current_user = User(valid_user)

#infinite loop
execution_loop = True
while execution_loop:

	command = input("> ")

	if command == "q":
		#end loop
		execution_loop = False

	if command == "man":
		#show extended manual
		current_user.man()

	if command == "mine":
		#mine the blockchain
		current_user.mine()
		print("You mined a block!")

	if command == "send_transaction":
		#send a transaction to another person (may or may not be registered)
		receiver = input("Addressee: ")
		amount = int(input("Enter integer amount: "))
		current_user.send_transaction(receiver, amount)
