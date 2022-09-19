#!/bin/sh

#redirect standard output to not print anything
#

#ROOT CERTIFICATE
#generate root certificate authority
openssl ecparam -genkey -name prime256v1 -out ../blockchain_storage/root/root.pem 
#convert to pkcs8
openssl pkcs8 -topk8 -in ../blockchain_storage/root/root.pem -out ../blockchain_storage/root/root-pkcs8.pem -nocrypt 
mv ../blockchain_storage/root/root-pkcs8.pem ../blockchain_storage/root/root.pem 
#auto sign (root)
openssl req -x509 -new -sha256 -nodes -key ../blockchain_storage/root/root.pem -days 3650 -out ../blockchain_storage/root/root.crt -subj "/C=ES/ST=MAD/L=MAD/O=Blockchain/CN=blockchain_root"  


#SUBOORDINATE CERTIFICATE AUTHORITY
#create subordinate certificate authority
openssl ecparam -genkey -name prime256v1 -out ../blockchain_storage/certificate/hostkey.pem 
#convert hosts private key to pkcs8
openssl pkcs8 -topk8 -in ../blockchain_storage/certificate/hostkey.pem -out ../blockchain_storage/certificate/hostkey-pkcs8.pem -nocrypt 
mv ../blockchain_storage/certificate/hostkey-pkcs8.pem ../blockchain_storage/certificate/hostkey.pem 
#create certificate request
openssl req -new -key ../blockchain_storage/certificate/hostkey.pem -nodes -out ../blockchain_storage/certificate/hostkey.csr -subj="/C=ES/ST=MAD/L=MAD/O=Blockchain/CN=blockchain_host" 
#sign subordinate authority request with root certificate authority
openssl x509 -req -sha256 -days 730 -in ../blockchain_storage/certificate/hostkey.csr -CA ../blockchain_storage/root/root.crt -CAkey ../blockchain_storage/root/root.pem -CAcreateserial -out ../blockchain_storage/certificate/hostkey.crt 


#VERIFICATION
#verify subordinate with root
openssl verify -CAfile ../blockchain_storage/root/root.crt ../blockchain_storage/certificate/hostkey.crt 

#CHAINING
cat ../blockchain_storage/root/root.crt ../blockchain_storage/certificate/hostkey.crt > ../blockchain_storage/certificate/hostkey_root_chain.crt 
#verify the chain
openssl verify -CAfile ../blockchain_storage/root/root.crt ../blockchain_storage/certificate/hostkey_root_chain.crt 


#remove residual files
rm ../blockchain_storage/root/root.srl ../blockchain_storage/certificate/hostkey.csr 


