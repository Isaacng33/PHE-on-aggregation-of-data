# app/encryption.py
'''Encryption Module'''
import os
import json
from phe import paillier

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'keys')


def generate_keys():
    '''
    Generates PaillierPublicKey and PaillierPrivateKey Object
    Stores it in keys directory
    Returns True or False
    '''
    try:
        # Ensure the keys directory exists
        os.makedirs(KEY_DIR, exist_ok=True)

        public_key, private_key = paillier.generate_paillier_keypair()

        # Save public key
        with open(os.path.join(KEY_DIR, 'public_key.pem'), 'w', encoding='utf-8') as f:
            json.dump({'n': str(public_key.n)}, f, indent=4)

        # Save private key with restricted permissions
        with open(os.path.join(KEY_DIR, 'private_key.pem'), 'w', encoding='utf-8') as f:
            json.dump({
                'p': str(private_key.p),
                'q': str(private_key.q)
            }, f, indent=4)

        print(f"Keys generated and saved to {KEY_DIR}")
        return True

    except Exception as e:  # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")

    return False

def load_public_key():
    '''
    Loads the Paillier public key from .pem file.
    Returns a PaillierPublicKey object.
    '''
    try:
        with open(os.path.join(KEY_DIR, 'public_key.pem'), 'r', encoding='utf-8') as f:
            public_key_data = json.load(f)
        n = int(public_key_data['n'])
        public_key = paillier.PaillierPublicKey(n)
        return public_key
    except FileNotFoundError:
        print("Public key file not found")
        return None

def load_private_key():
    '''
    Loads the Paillier private key from .pem file
    Returns a PaillierPrivateKey object
    '''
    try:
        with open(os.path.join(KEY_DIR, 'private_key.pem'), 'r', encoding='utf-8') as f:
            private_key_data = json.load(f)
        p = int(private_key_data['p'])
        q = int(private_key_data['q'])

        private_key = paillier.PaillierPrivateKey(load_public_key(), p, q)

        return private_key
    except FileNotFoundError:
        print("Private key file not found")
        return None

def encrypt_number(public_key, number):
    '''
    Encrypts a number based on a Paillier public key
    Returns an encrypted value (EncryptedNumber)
    '''
    return public_key.encrypt(number)

def decrypt_number(private_key, encrypted_nunber):
    '''
    Decrypts an encrypted value with a Paillier private key
    Returns the int or float that EncryptedNumber was holding
    '''
    return private_key.decrypt(encrypted_nunber)
