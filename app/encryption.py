# app/encryption.py
from phe import paillier

# Function to generate public and private key
def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

# Function to encrypt a number
def encrypt_number(public_key, number):
    return public_key.encrypt(number)

# Function to decrypt a encrypted number
def decrypt_number(private_key, encrypted_nunber):
    return private_key.decrypt(encrypted_nunber)