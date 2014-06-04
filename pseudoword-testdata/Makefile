
#OPENSSL_INCLUDE = ~/tools/openssl-1.0.1f/include/
#OPENSSL_LIB = ~/tools/openssl-1.0.1f/libcrypto.a
keyname: keyname.c
	gcc -O4 -std=c99 keyname.c -lcrypto -o keyname

test:
	python ./keyname_script.py 