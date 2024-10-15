#tests/test_encryption.py
'''Module to test encryption methods'''
from app.encryption import generate_keys, encrypt_number, decrypt_number

def test_encryption_decryption():
    '''Checks if the encryption and decryption method works'''
    public_key, private_key = generate_keys()
    number = 123
    encrypted = encrypt_number(public_key, number)
    decrypted = decrypt_number(private_key, encrypted)
    assert decrypted == number
