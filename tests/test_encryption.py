#tests/test_encryption.py
'''Module to test encryption methods'''
import os
from app.encryption import (
    KEY_DIR,
    generate_keys,
    load_context_public,
    load_secret,
    encrypt_int,
    decrypt_int
)

def test_generate_keys():
    '''Test for key'''
    # Ensure the keys directory is empty before the test
    for file in os.listdir(KEY_DIR):
        os.remove(os.path.join(KEY_DIR, file))

    # Call the generate_keys function
    result = generate_keys(30)

    # Check if the function returned True
    assert result is True

    # Check if the files are not empty
    assert os.path.getsize(os.path.join(KEY_DIR, 'context.pkl')) > 0
    assert os.path.getsize(os.path.join(KEY_DIR, 'public_key.pkl')) > 0
    assert os.path.getsize(os.path.join(KEY_DIR, 'secret_key.pkl')) > 0

def test_load_context_public():
    '''Ensure load public key & context function works'''
    encryption_obj = load_context_public()
    assert encryption_obj is not None

def test_load_secret_key():
    '''Ensure load private key function works'''
    encryption_obj = load_context_public()
    assert encryption_obj is not None

    assert load_secret(encryption_obj) is not None

def test_encrypt_int():
    '''Ensure encryption of an integer works'''
    encryption_obj = load_context_public()
    assert encryption_obj is not None

    data = [10, -10, 0, 42, -42, 12345, -12345, 1000000, -1000000]
    for integer in data:
        ciphertext = encrypt_int(encryption_obj, integer)
        assert ciphertext is not None, (F"Encryption failed for integer {integer}")
        print(f"Test passed for encryption integer: {integer}, Encrypted data: {ciphertext}")
    print("All test case passed for encryption")

def test_decrypt_int():
    '''Ensure decryption of an integer works'''
    encryption_obj = load_context_public()
    assert encryption_obj is not None

    key = load_secret(encryption_obj)
    assert key is not None

    # Encryption data set
    data = [10, -10, 0, 42, -42, 12345, -12345, 1000000, -1000000]
    for integer in data:
        ciphertext = encrypt_int(encryption_obj, integer)
        assert ciphertext is not None

        decrypted_int = decrypt_int(key, ciphertext)
        if decrypted_int != integer:
            print(f"Integer: {integer}, Decrypted integer: {decrypted_int}")
        assert decrypted_int == integer, (f"Decryption failed for integer {integer}")
        print(f"Test passed for decryption integer: {integer}, Decrypted data: {decrypted_int}")
    print("All test case passed for decryption")

def clear_keys():
    '''Clean up after the tests'''
    for file in os.listdir(KEY_DIR):
        file_path = os.path.join(KEY_DIR, file)
        if os.path.isfile(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.truncate(0)
