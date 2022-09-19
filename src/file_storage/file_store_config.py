"""Module with configuration constants"""

#BLOCKCHAIN STORAGE
BLOCKCHAIN_LOG_FILE = "blockchainLogStore.json"
BLOCKCHAIN_STORAGE_PATH = "../blockchain_storage/"
ROOT_FOLDER_PATH = "../blockchain_storage/root/"
PUBLIC_KEYS_FOLDER_PATH = "../blockchain_storage/public_keys/"
CERTIFICATES_FOLDER_PATH = "../blockchain_storage/certificate/"
ROOT_KEY = "root"

#USER LOCAL STORAGE
LOCAL_HOST_PUBLIC = "../host/public/"
LOCAL_HOST_PRIVATE = "../host/private/"

#CERTIFICATE AUTHORITIES SOURCE CODE
GIVE_PERMISSIONS = "chmod u+x"
EXECUTE = "./"
KEY_FILE_EXTENSION = ".pem"
CERTIFICATE_FILE_EXTENSION = ".crt"
CA_SCRIPT_FILE = "certificate_authorities/certification_authorities.sh"
CREATE_KEYS_CA_FILE = "certificate_authorities/create_keys.sh"
CHANGE_NAMES_FILE = "certificate_authorities/change_name.sh"
HOST_PRIVATE_KEY = "hostkey"
PUBLIC_KEY_FILE_AUX = "key_public"
KEY_FILE_AUX = "key"

 