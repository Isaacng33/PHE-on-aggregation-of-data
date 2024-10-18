# app/encryption.py
'''Encryption Module'''
import os
import numpy as np
from Pyfhel import Pyfhel

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'keys')


def generate_keys(t_value=20):
    '''
    Generates Pyfhel context, public and private keys, and saves them to files.
    Returns True if successful, False otherwise.

    Args:
        t_value: specified plaintext modulus t
    '''
    try:
        # Ensure the keys directory exists
        os.makedirs(KEY_DIR, exist_ok=True)

        encryption_obj = Pyfhel()
        encryption_obj.contextGen(scheme='bfv', n=2**14, t_bits=t_value)
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

def load_secret(encryption_obj):
    '''
    Loads the secret key for an existing Pyfhel object
    Returns True if successful, False otherwise
    '''
    try:
        encryption_obj.load_secret_key(os.path.join(KEY_DIR, 'secret_key.pkl'))
        return encryption_obj
    except FileNotFoundError:
        print("Secret key file not found")
        return None

def encrypt_int(encryption_obj, integer):
    '''
    Encrypts an integer using public key in object

    Args:
        encryption_obj: Pyfhel object
        integer: Int to encrypt

    Returns:
        PyCtxt: An encrypted ciphertext of the input integer
    '''
    try:
        int_array = np.array([integer], dtype=np.int64)
        ciphertext = encryption_obj.encrypt(int_array)
        return ciphertext
    except Exception as e:
        print(f"An error occurred while encrypting: {e}")
        return None

def decrypt_int(encryption_obj, ciphertext):
    '''
    Decrypts an encrypted integer using the secret key in the Pyfhel object.

    Args:
        encryption_obj: Pyfhel object with the secret key loaded.
        ciphertext: PyCtxt, the encrypted integer to decrypt.

    Returns:
        Integer: The decrypted integer, or None if decryption fails.
    '''
    try:
        decrypted_array = encryption_obj.decrypt(ciphertext)
        integer = int(decrypted_array[0])
        return integer
    except Exception as e:
        print(f"An error occurred while decrypting: {e}")
        return None
