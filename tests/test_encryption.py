#tests/test_encryption.py
'''Module to test encryption methods'''
import os
import numpy as np
from app.encryption import (
    KEY_DIR,
    generate_keys,
    load_context_public,
    load_secret,
    encrypt_value,
    decrypt_value,
    add_encrypted,
    sub_encrypted,
    multiply_encrypted
)

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
    assert os.path.getsize(os.path.join(KEY_DIR, 'relin_key.pkl')) > 0
    assert os.path.getsize(os.path.join(KEY_DIR, 'rotate_key.pkl')) > 0

def test_load_context_public():
    '''Ensure load public key & context function works'''
    encryption_obj = load_context_public()
    assert encryption_obj is not None

def test_load_secret_key():
    '''Ensure load private key function works'''
    encryption_obj = load_context_public()
    assert load_secret(encryption_obj) is not None

def test_encrypt_value():
    '''Ensure encryption of an integer works'''
    encryption_obj = load_context_public()

    data = np.array([10.5, -10.5, 0.0, 42.42, -42.42, 12345.678, -12345.678], dtype=np.float64)
    for number in data:
        ciphertext = encrypt_value(encryption_obj, number)
        assert ciphertext is not None, (F"Encryption failed for number {number}")
        print(f"Test passed for encryption integer: {number}, Encrypted data: {ciphertext}")
    print("All test case passed for encryption\n")

def test_decrypt_value():
    '''Ensure decryption of a float works'''
    encryption_obj = load_context_public()
    encryption_obj = load_secret(encryption_obj)

    # Encryption data set
    data = np.array([10.5, -10.5, 0.0, 42.42, -42.42, 12345.678, -12345.678], dtype=np.float64)
    for number in data:
        ciphertext = encrypt_value(encryption_obj, number)
        decrypted_number = decrypt_value(encryption_obj, ciphertext)
        assert decrypted_number is not None, f"Decryption failed for number {number}."
        assert abs(decrypted_number - number) < 1e-3, (
            f"Decryption mismatch: {decrypted_number} vs {number}"
        )
        print(f"Test passed for decryption number: {number}, Decrypted data: {decrypted_number:.3f}")
    print("All test cases passed for decryption.\n")

def test_add_encrypted():
    '''Ensure addition in encrypted form works'''
    encryption_obj = load_context_public()
    encryption_obj = load_secret(encryption_obj)

    # Encryption data set
    data = np.array([10.5, -10.5, 0.0, 42.42, -42.42, 12345.678, -12345.678], dtype=np.float64)

    for i in range(len(data) - 1):
        num1 = data[i]
        num2 = data[i + 1]
        expected_sum = num1 + num2

        ciphertext_1 = encrypt_value(encryption_obj, num1)
        ciphertext_2 = encrypt_value(encryption_obj, num2)

        ciphertext_sum = add_encrypted(ciphertext_1, ciphertext_2)
        decrypted_sum = decrypt_value(encryption_obj, ciphertext_sum)

        assert is_within_tolerance(expected_sum, decrypted_sum), (
            f"Subtraction mismatch: {decrypted_sum} vs {expected_sum}"
        )
        print(f"Test passed for addition of {num1} and {num2}: Decrypted sum {decrypted_sum:.3f}")
    print("All test cases passed for encrypted addition.\n")

def test_sub_encrypted():
    '''Ensure subtraction in encrypted form works'''
    encryption_obj = load_context_public()
    encryption_obj = load_secret(encryption_obj)

    # Encryption data set
    data = np.array([10.5, -10.5, 0.0, 42.42, -42.42, 12345.678, -12345.678], dtype=np.float64)

    for i in range(len(data) - 1):
        num1 = data[i]
        num2 = data[i + 1]
        expected_sum = num1 - num2

        ciphertext_1 = encrypt_value(encryption_obj, num1)
        ciphertext_2 = encrypt_value(encryption_obj, num2)

        ciphertext_sum = sub_encrypted(ciphertext_1, ciphertext_2)
        decrypted_sum = decrypt_value(encryption_obj, ciphertext_sum)

        assert is_within_tolerance(expected_sum, decrypted_sum), (
            f"Subtraction mismatch: {decrypted_sum} vs {expected_sum}"
        )
        print(f"Test passed for subtraction of {num1} and {num2}: Decrypted sum {decrypted_sum:.3f}")
    print("All test cases passed for encrypted subtraction.\n")

def test_multiply_encrypted():
    '''Ensure multiplication in encrypted form works'''
    encryption_obj = load_context_public()
    encryption_obj = load_secret(encryption_obj)

    # Encryption data set
    data = np.array([10.5, -10.5, 0.0, 42.42, -42.42, 12345.678, -12345.678], dtype=np.float64)

    for i in range(len(data) - 1):
        num1 = data[i]
        num2 = data[i + 1]
        expected_product = num1 * num2

        ciphertext_1 = encrypt_value(encryption_obj, num1)
        ciphertext_2 = encrypt_value(encryption_obj, num2)

        ciphertext_product = multiply_encrypted(encryption_obj, ciphertext_1, ciphertext_2)
        decrypted_product = decrypt_value(encryption_obj, ciphertext_product)

        assert is_within_tolerance(expected_product, decrypted_product), (
            f"Multiplication mismatch: {decrypted_product} vs {expected_product}"
        )
        print(f"Test passed for multiplication of {num1} and {num2}: Decrypted product {decrypted_product:.3f}")
    print("All test cases passed for encrypted multiplication.\n")

def is_within_tolerance(expected, decrypted, absolute_tol=1e-3, relative_tol=1e-3):
    '''
    Checks if the decrypted value is within acceptable error bounds of the expected value.

    Args:
        expected: The expected float value.
        decrypted: The decrypted float value.
        absolute_tol: The maximum allowable absolute error.
        relative_tol: The maximum allowable relative error.

    Returns:
        bool: True if within tolerance, False otherwise.
    '''
    if abs(expected) < 1e-6:
        return abs(decrypted - expected) < absolute_tol
    return (abs(decrypted - expected) / abs(expected) < relative_tol)

def clear_keys():
    '''Clean up after the tests'''
    for file in os.listdir(KEY_DIR):
        file_path = os.path.join(KEY_DIR, file)
        if os.path.isfile(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.truncate(0)

