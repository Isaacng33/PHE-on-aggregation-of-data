#tests/test_encryption.py
'''Module to test encryption methods'''
import os
from app.encryption import generate_keys, KEY_DIR, load_context_public, load_secret_key

def test_generate_keys():
    '''Test for key'''
    # Ensure the keys directory is empty before the test
    for file in os.listdir(KEY_DIR):
        os.remove(os.path.join(KEY_DIR, file))

    # Call the generate_keys function
    result = generate_keys()

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

    assert load_secret_key(encryption_obj) is True


def clear_keys():
    '''Clean up after the tests'''
    for file in os.listdir(KEY_DIR):
        file_path = os.path.join(KEY_DIR, file)
        if os.path.isfile(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.truncate(0)
