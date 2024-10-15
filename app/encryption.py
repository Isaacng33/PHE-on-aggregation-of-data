# app/encryption.py
'''Encryption Module'''
from phe import paillier

def generate_keys():
    '''Method to generate public and private key'''
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def encrypt_number(public_key, number):
    '''Method to encrypt number'''
    return public_key.encrypt(number)

def decrypt_number(private_key, encrypted_nunber):
    '''Method to decrypt a encrypted number'''
    return private_key.decrypt(encrypted_nunber)
