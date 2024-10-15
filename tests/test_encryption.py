#tests/test_encryption.py
import pytest
from app.encryption import generate_keys, encrypt_number, decrypt_number

# Checks if the encrypt and decrypt method works
def test_encryption_decryption():
    public_key, private_key = generate_keys()
    number = 123
    encrypted = encrypt_number(public_key, number)
    decrypted = decrypt_number(private_key, encrypted)
    assert decrypted == number