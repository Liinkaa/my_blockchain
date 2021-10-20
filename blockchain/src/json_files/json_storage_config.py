"""Module with configuration and constants"""

from pathlib import Path

JSON_FILES_PATH = str(Path.home()) + "/Desktop/blockchain/storage/"
WALLET_FILES_PATH = str(Path.home()) + "/Desktop/blockchain/storage/wallet_booklets/"
REGISTRATION_FILE = "accountsStore.json"
BLOCKCHAIN_LOG_FILE = "blockchainLogStore.json"
EXTENSION_FILE = ".json"