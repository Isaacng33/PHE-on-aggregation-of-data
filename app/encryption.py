# app/encryption.py
'''Encryption Module'''
import os
import numpy as np
from Pyfhel import Pyfhel

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'keys')


def generate_keys(n_value=2**14, scale_bits=30):
    '''
    Generates Pyfhel context, public and private keys for CKKS, and saves them to files.
    Returns True if successful, False otherwise.

    Args:
        n_value: polynomial modulus degree (must be a power of 2)
        scale_bits: bits of precision for the scaling factor
    '''
    try:
        # Ensure the keys directory exists
        os.makedirs(KEY_DIR, exist_ok=True)

        ckks_params = {
            'scheme': 'CKKS',   # can also be 'ckks'
            'n': n_value,         # Polynomial modulus degree. For CKKS, n/2 values can be
                                #  encoded in a single ciphertext.
                                #  Typ. 2^D for D in [10, 15]
            'scale': 2**scale_bits,     # All the encodings will use it for float->fixed point
                                #  conversion: x_fix = round(x_float * scale)
                                #  You can use this as default scale or use a different
                                #  scale on each operation (set in HE.encryptFrac)
            'qi_sizes': [60, 30, 30, 30, 60]
        }

        encryption_obj = Pyfhel()
        encryption_obj.contextGen(**ckks_params)
        encryption_obj.keyGen()
        encryption_obj.relinKeyGen()
        encryption_obj.rotateKeyGen()

        # Save context and keys
        encryption_obj.save_context(os.path.join(KEY_DIR, 'context.pkl'))
        encryption_obj.save_public_key(os.path.join(KEY_DIR, 'public_key.pkl'))
        encryption_obj.save_secret_key(os.path.join(KEY_DIR, 'secret_key.pkl'))
        encryption_obj.save_relin_key(os.path.join(KEY_DIR, 'relin_key.pkl'))
        encryption_obj.save_rotate_key(os.path.join(KEY_DIR, 'rotate_key.pkl'))

        print(f"CKKS Context and Keys generated and saved to {KEY_DIR}")
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
        encryption_obj.load_relin_key(os.path.join(KEY_DIR, 'relin_key.pkl'))
        encryption_obj.load_rotate_key(os.path.join(KEY_DIR, 'rotate_key.pkl'))
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

def encrypt_value(encryption_obj, value):
    '''
    Encrypts a float using the CKKS scheme in the Pyfhel object.

    Args:
        encryption_obj: Pyfhel object
        value: Float to encrypt

    Returns:
        PyCtxt: An encrypted ciphertext of the input float
    '''
    try:
        ciphertext = encryption_obj.encrypt(value)
        return ciphertext
    except Exception as e:
        print(f"An error occurred while encrypting: {e}")
        return None

def decrypt_value(encryption_obj, ciphertext):
    '''
    Decrypts an encrypted float using the secret key in the Pyfhel object.

    Args:
        encryption_obj: Pyfhel object with the secret key loaded.
        ciphertext: PyCtxt, the encrypted value to decrypt.

    Returns:
        List: A list where the decrypted value is loacted in the [0] index
    '''
    try:
        value = encryption_obj.decrypt(ciphertext)
        return value[0]
    except Exception as e:
        print(f"An error occurred while decrypting: {e}")
        return None

def add_encrypted(ciphertext_1, ciphertext_2):
    '''
    Performs addition on 2 encrypted value

    Args:
        2 encrypted PyCtxt Object
    
    Returns:
        Sum: PyCtxt object 
    '''
    return ciphertext_1 + ciphertext_2

def sub_encrypted(ciphertext_1, ciphertext_2):
    '''
    Performs subtraction on 2 encrypted value

    Args:
        2 encrypted PyCtxt Object
    
    Returns:
        Sum: PyCtxt object 
    '''
    return ciphertext_1 - ciphertext_2
