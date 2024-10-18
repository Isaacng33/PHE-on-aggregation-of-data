# app/encryption.py
'''Encryption Module'''
import os
from Pyfhel import Pyfhel

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'keys')


def generate_keys():
    '''
    Generates Pyfhel context, public and private keys, and saves them to files.
    Returns True if successful, False otherwise.
    '''
    try:
        # Ensure the keys directory exists
        os.makedirs(KEY_DIR, exist_ok=True)

        encryption_obj = Pyfhel()
        encryption_obj.contextGen(scheme='bfv', n=2**14, t_bits=20)
        encryption_obj.keyGen()

        # Save context and keys
        encryption_obj.save_context(os.path.join(KEY_DIR, 'context.pkl'))
        encryption_obj.save_public_key(os.path.join(KEY_DIR, 'public_key.pkl'))
        encryption_obj.save_secret_key(os.path.join(KEY_DIR, 'secret_key.pkl'))

        print(f"Context and Keys generated and saved to {KEY_DIR}")
        return True
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return False

def load_context_public():
    '''
    Loads Context and Public keys from files
    Returns a Pyfhel object with public context
    '''
    try:
        encryption_obj = Pyfhel()
        encryption_obj.load_context(os.path.join(KEY_DIR, 'context.pkl'))
        encryption_obj.load_public_key(os.path.join(KEY_DIR, 'public_key.pkl'))
        return encryption_obj
    except FileNotFoundError:
        print("One or more public Pyfhel files not found")
        return None

def load_secret_key(encryption_obj):
    '''
    Loads the secret key for an existing Pyfhel object
    Returns True if successful, False otherwise
    '''
    try:
        encryption_obj.load_secret_key(os.path.join(KEY_DIR, 'secret_key.pkl'))
        return True
    except FileNotFoundError:
        print("Secret key file not found")
        return False
