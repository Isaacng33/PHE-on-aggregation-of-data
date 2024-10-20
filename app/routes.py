# app/routes.py
'''Module to handle API Routes'''
import os
import pandas as pd
import pickle
import gzip
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
    Encrypts all financial data (Income, Expenses, etc.) in the dataset and saves it to a new binary file.
    Utilizes batching to optimize storage.
    """
    encrypted_dataset = []

    # Iterate over all rows and encrypt the financial fields using batching
    for _, row in financial_data.iterrows():
        financial_values = [
            row['Income (£)'],
            row['Expenses (£)'],
            row['Savings (£)'],
            row['Investments (£)'],
            row['Loans (£)']
        ]
        ciphertext = encrypt_value(encryption_obj, financial_values)
        if ciphertext is not None:
            serialized_ciphertext = serialised_encrypted(ciphertext)
            encrypted_row = {
                'User ID': row['User ID'],
                'Encrypted Financials': serialized_ciphertext
            }
            encrypted_dataset.append(encrypted_row)
        else:
            print(f"Encryption failed for User ID: {row['User ID']}")

    # Serialize and save the entire encrypted dataset using Pickle and Gzip
    try:
        save_path = os.path.join(os.path.dirname(__file__), '..', 'data/encrypted_financial_data.pkl.gz')
        with gzip.open(save_path, 'wb') as file:
            pickle.dump(encrypted_dataset, file)
        print(f"Encrypted data saved to {save_path}")
        return jsonify({"message": "All data encrypted and saved to a new binary file."}), 200
    except Exception as e:
        print(f"An error occurred while saving encrypted data: {e}")
        return jsonify({"error": "Failed to save encrypted data."}), 500

@main.route('/decrypt_all', methods=['GET'])
def decrypt_all():
    """
    Decrypts all encrypted financial data in the dataset.
    Verifies data integrity by decrypting and displaying the raw data.
    """
    load_secret(encryption_obj)

    # Path to the encrypted data binary file
    encrypted_data_path = os.path.join(os.path.dirname(__file__), '..', 'data/encrypted_financial_data.pkl.gz')

    # Load the encrypted dataset
    try:
        with gzip.open(encrypted_data_path, 'rb') as file:
            encrypted_dataset = pickle.load(file)
    except FileNotFoundError:
        print("Encrypted data file not found.")
        return jsonify({"error": "Encrypted data file not found."}), 404
    except Exception as e:
        print(f"An error occurred while loading encrypted data: {e}")
        return jsonify({"error": "Failed to load encrypted data."}), 500

    decrypted_dataset = []

    # Iterate over all rows and decrypt the financial fields
    for row in encrypted_dataset:
        try:
            serialized_ciphertext = row['Encrypted Financials']
            ciphertext = deserialised(serialized_ciphertext.encode('utf-8'), encryption_obj)
            if ciphertext is not None:
                decrypted_values = decrypt_value(encryption_obj, ciphertext)
                decrypted_row = {
                    'User ID': row['User ID'],
                    'Decrypted Income': f"{decrypted_values[0]:.2f}",
                    'Decrypted Expenses': f"{decrypted_values[1]:.2f}",
                    'Decrypted Savings': f"{decrypted_values[2]:.2f}",
                    'Decrypted Investments': f"{decrypted_values[3]:.2f}",
                    'Decrypted Loans': f"{decrypted_values[4]:.2f}"
                }
                decrypted_dataset.append(decrypted_row)
            else:
                print(f"Deserialization failed for User ID: {row['User ID']}")
        except Exception as e:
            print(f"An error occurred while decrypting User ID {row['User ID']}: {e}")

    # Create a new DataFrame from the decrypted dataset
    decrypted_df = pd.DataFrame(decrypted_dataset)

    # Display the decrypted data in a readable format (optional)
    print(tabulate(decrypted_df, headers='keys', tablefmt='pretty'))

    return jsonify({"message": "All data decrypted and displayed."}), 200
