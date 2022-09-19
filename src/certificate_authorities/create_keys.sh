#!/bin/sh

#redirect standard output to not print anything
#

#create key
openssl ecparam -genkey -name prime256v1 | openssl ec -aes256 -out ../host/private/key.pem -passout pass:$1 
#convert to pkcs8
openssl pkcs8 -topk8 -inform PEM -outform PEM -passin pass:$1 -in ../host/private/key.pem -out ../host/private/key-pkcs8.pem -passout pass:$1 
mv ../host/private/key-pkcs8.pem ../host/private/key.pem 
#create certificate request
openssl req -new -key ../host/private/key.pem -passin pass:$1 -nodes -out ../host/private/key.csr -subj="/C=ES/ST=MAD/L=MAD/O=Blockchain/CN=user" 
#sign key request with hostkey certificate authority (output certification to the host)
openssl x509 -req -sha256 -days 730 -in ../host/private/key.csr -passin pass:$1 -CA ../blockchain_storage/certificate/hostkey.crt -CAkey ../blockchain_storage/certificate/hostkey.pem -CAcreateserial -out ../host/certificate/key.crt 
#extract public key
openssl ec -in ../host/private/key.pem -passin pass:$1 -pubout -out ../host/public/key_public.pem 

#remove all generated files
rm ../host/private/key.csr ../blockchain_storage/certificate/hostkey.srl 


