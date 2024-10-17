#tests/test_encryption.py
'''Module to test encryption methods'''
import pytest
from app.encryption import (
    generate_keys,
    encrypt_number,
    decrypt_number,
    load_private_key,
    load_public_key
)


@pytest.fixture(scope="module")
def key_pair():
    '''Fixture to generate and load keys'''
    assert generate_keys(), "Generation failed: Keys failed to generate"
    public_key = load_public_key()
    private_key = load_private_key()
    assert public_key is not None, "Load failed: Public Key failed to load"
    assert private_key is not None, "Load failed: Private Key failed to load"
    return public_key, private_key

def test_encryption(key_pair):
    '''Test that encryption changes the original value.'''
    public_key, _ = key_pair
    original_value = 123
    encrypted_value = encrypt_number(public_key, 123)
    assert encrypted_value != original_value, (
        "Encryption failed: Encrypted value equals the original."
    )

def test_decryption(key_pair):
    '''Test that decryption retrieves the original value.'''
    public_key, private_key = key_pair
    original_value = 123
    encrypted_value = encrypt_number(public_key, original_value)
    decrypted_value = decrypt_number(private_key, encrypted_value)
    assert decrypted_value == original_value, (
        "Decryption failed: Decrypted value does not match the original."
    )
