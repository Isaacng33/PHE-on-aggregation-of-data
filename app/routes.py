# app/routes.py
'''Module to handle API Routes'''
import os
import pandas as pd
from tabulate import tabulate
from flask import Blueprint, jsonify
from app.encryption import (
    generate_keys,
    load_context_public,
    load_secret,
    encrypt_value,
    decrypt_value,
    add_encrypted,
    sub_encrypted,
    multiply_encrypted,
    serialised_encrypted,
    deserialised
)

main = Blueprint('main', __name__)

# Financial Data FIle Dir
data_path = os.path.join(os.path.dirname(__file__), '..', 'data/financial_data.csv')
financial_data = pd.read_csv(data_path)

# Initilise encryption context
generate_keys()
encryption_obj = load_context_public()

@main.route('/encrypt_all', methods=['GET'])
def encrypt_all():
    """
    In a real world scenario, we expect the data to be encrypted already
    Function here is to simulate the real world situation
    Route to encrypt all financial data (Income, Expenses, etc.) in the dataset and save it to a new file.
    """
    encrypted_dataset = []
    # Iterate over all rows and encrypt the financial fields
    for _, row in financial_data.iterrows():
        encrypted_row = {
            'User ID': row['User ID'],
            'Encrypted Income': serialised_encrypted(encrypt_value(encryption_obj, row['Income (£)'])),
            'Encrypted Expenses': serialised_encrypted(encrypt_value(encryption_obj, row['Expenses (£)'])),
            'Encrypted Savings': serialised_encrypted(encrypt_value(encryption_obj, row['Savings (£)'])),
            'Encrypted Investments': serialised_encrypted(encrypt_value(encryption_obj, row['Investments (£)'])),
            'Encrypted Loans': serialised_encrypted(encrypt_value(encryption_obj, row['Loans (£)']))
        }
        encrypted_dataset.append(encrypted_row)

    # Create a new DataFrame from the encrypted dataset
    encrypted_df = pd.DataFrame(encrypted_dataset)
    print(tabulate(encrypted_df, headers='keys', tablefmt='pretty'))

    # Save the encrypted DataFrame to a new CSV file
    new_data_path = os.path.join(os.path.dirname(__file__), '..', 'data/encrypted_financial_data.csv')
    encrypted_df.to_csv(new_data_path, index=False)

    return jsonify({"message": "All data encrypted and saved to a new file."}), 200

@main.route('/decrypt_all', methods=['GET'])
def decrypt_all():
    """
    Route to decrypt all encrypted financial data in the dataset.
    Never really necessary since we will not access the raw data rather we only need the aggregated result
    Function just to verify that the raw data integrity is there
    """
    # Path to the encrypted data CSV file
    encrypted_data_path = os.path.join(os.path.dirname(__file__), '..', 'data/encrypted_financial_data.csv')

    # Load the encrypted dataset
    encrypted_df = pd.read_csv(encrypted_data_path)

    decrypted_dataset = []

    load_secret(encryption_obj)
    # Iterate over all rows and decrypt the financial fields
    for _, row in encrypted_df.iterrows():
        decrypted_row = {
            'User ID': row['User ID'],
            'Decrypted Income': decrypt_value(encryption_obj, deserialised(row['Encrypted Income'], encryption_obj)),
            'Decrypted Expenses': decrypt_value(encryption_obj, deserialised(row['Encrypted Expenses'], encryption_obj)),
            'Decrypted Savings': decrypt_value(encryption_obj, deserialised(row['Encrypted Savings'], encryption_obj)),
            'Decrypted Investments': decrypt_value(encryption_obj, deserialised(row['Encrypted Investments'], encryption_obj)),
            'Decrypted Loans': decrypt_value(encryption_obj,deserialised( row['Encrypted Loans'], encryption_obj))
        }
        decrypted_dataset.append(decrypted_row)

    decrypted_df = pd.DataFrame(decrypted_dataset)
    # Format each numerical column to 2 decimal places
    float_columns = ['Decrypted Income', 'Decrypted Expenses', 'Decrypted Savings', 'Decrypted Investments', 'Decrypted Loans']
    for col in float_columns:
        decrypted_df[col] = decrypted_df[col].apply(lambda x: f"{x:.2f}")

    print(tabulate(decrypted_df, headers='keys', tablefmt='pretty'))
    return jsonify({"message": "All data decrypted and printed."}), 200
