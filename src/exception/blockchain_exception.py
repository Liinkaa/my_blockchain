"""Module with customized version of exception for the blockchain"""

class BlockchainException(Exception):
    
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """gets the message value"""
        return self.__message

    @message.setter
    def message(self, value):
        """sets the message value"""
        self.__message = value
