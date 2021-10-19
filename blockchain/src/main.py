"""Module with main execution program"""

from access import AccountManagement

print("Hi! Welcome to the BlockChain Simulator\n")
print("Press 1 to Register\nPress 2 to Login\n")

#Instantiate account management for the session
current_user_management = AccountManagement()

advance = False
while advance == False:
	print("Please enter either 1 or 2\n")
	select = int(input())

	if select == 1:
		#create a new user
		print("Create user: \n")
		username = str(input("Username: "))
		print("\n")
		password = str(input("Password: "))

		current_user_management.register(username, password)

		print("Successfully registered")
		advance = True

	elif select == 2:
		#access existing account
		print("Login: \n")
		username = str(input("Username: "))
		print("\n")
		password = str(input("Password: "))

		if(current_user_management.access(username, password)<0):
			print("User not registered")
		else:
			advance = True

