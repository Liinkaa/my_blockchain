#!/bin/sh

#receive input name in $1 public_key, $2 private_key
#change the names and create copies in the blockchain

#change name of private key with hash of generated private key
mv ../host/private/key.pem ../host/private/$2.pem 
#change the name of the certificate with the hash of the public key
mv ../host/certificate/key.crt ../host/certificate/$1.crt 
#copy the certificate into the blockchain
cp ../host/certificate/$1.crt ../blockchain_storage/certificate/$1.crt 
#change name of public key  with the hash of the public key
mv ../host/public/key_public.pem ../host/public/$1.pem 
#copy the public key into the blockchain
cp ../host/public/$1.pem ../blockchain_storage/public_keys/$1.pem 

