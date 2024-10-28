# app/routes.py
'''Module to handle API Routes'''
import os
import pandas as pd
import pickle
import gzip
import json
from tabulate import tabulate
from flask import Blueprint, jsonify
from Pyfhel import Pyfhel, PyCtxt
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
    Encrypts all financial data (Revenue, Expenses, etc.) in the dataset and saves it to a new binary file.
    Utilizes batching to optimize storage.
    """
    encrypted_dataset = []
    # Iterate over all rows and encrypt the financial fields using batching
    for _, row in financial_data.iterrows():
        financial_values = row.drop(labels=['Record ID']).values.tolist()
        ciphertext = encrypt_value(encryption_obj, financial_values)
        if ciphertext is not None:
            serialized_ciphertext = serialised_encrypted(ciphertext)
            encrypted_row = {
                'Record ID': row['Record ID'],
                'Encrypted Financials': serialized_ciphertext
            }
            encrypted_dataset.append(encrypted_row)
        else:
            print(f"Encryption failed for Record ID: {row['Record ID']}")

    # Save the entire encrypted dataset using Pickle and Gzip
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
    total_revenue, total_expenses, total_savings, total_investments, total_loans = 0.0, 0.0, 0.0, 0.0, 0.0

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
            ciphertext = deserialised(serialized_ciphertext, encryption_obj)
            if ciphertext is not None:
                decrypted_values = decrypt_value(encryption_obj, ciphertext)
                decrypted_row = {
                    'Decrypted Revenue': f"{decrypted_values[0]:.2f}",
                    'Decrypted Expenses': f"{decrypted_values[1]:.2f}",
                    'Decrypted Savings': f"{decrypted_values[2]:.2f}",
                    'Decrypted Investments': f"{decrypted_values[3]:.2f}",
                    'Decrypted Loans': f"{decrypted_values[4]:.2f}"
                }
                decrypted_dataset.append(decrypted_row)
                # Accumulate the decrypted sums for cross checking purposes
                total_revenue += decrypted_values[0]
                total_expenses += decrypted_values[1]
                total_savings += decrypted_values[2]
                total_investments += decrypted_values[3]
                total_loans += decrypted_values[4]
            else:
                print(f"Deserialization failed for Record ID: {row['Record ID']}")
        except Exception as e:
            print(f"An error occurred while decrypting Record ID {row['Record ID']}: {e}")

    # Create a new DataFrame from the decrypted dataset
    decrypted_df = pd.DataFrame(decrypted_dataset)

    # Display the decrypted data in a readable format (optional)
    print(tabulate(decrypted_df, headers='keys', tablefmt='pretty'))

    # Display sums
    total_sums = {
        'Total Revenue': f"{total_revenue:.2f}",
        'Total Expenses': f"{total_expenses:.2f}",
        'Total Savings': f"{total_savings:.2f}",
        'Total Investments': f"{total_investments:.2f}",
        'Total Loans': f"{total_loans:.2f}"
    }
    print("\nSummed Financials:")
    json_string = json.dumps(total_sums, indent=4)
    print(json_string)

    return jsonify({"message": "All data decrypted and displayed."}), 200

@main.route('/aggregation', methods=['GET'])
def aggregation():
    '''
    Homomorphically sums all the encrypted financial columns (Revenue, Expenses, etc.) before decrypting.
    Decrypted Print statements are just for checking purposes
    '''
    load_secret(encryption_obj)
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
    
    total = 0.0
    for row in encrypted_dataset:
        try:
            serialised_ciphertext = row['Encrypted Financials']
            ciphertext = deserialised(serialised_ciphertext, encryption_obj)
            if ciphertext is not None:
                total += ciphertext
            else:
                print(f"Deserialization failed for Record ID: {row['Record ID']}")
        except Exception as e:
            print(f"An error occurred while processing encrypted Record ID: {e}")

    # Prepare the result dict with the summed columns
    decrypted_value = decrypt_value(encryption_obj, total)
    summed_result = {
        'Total Revenue': f"{decrypted_value[0]:.2f}",
        'Total Expenses': f"{decrypted_value[1]:.2f}",
        'Total Savings': f"{decrypted_value[2]:.2f}",
        'Total Investments': f"{decrypted_value[3]:.2f}",
        'Total Loans': f"{decrypted_value[4]:.2f}",
    }

    print("\nSummed Financials:")
    json_string = json.dumps(summed_result, indent=4)
    print(json_string)

    serialised_ciphertext = serialised_encrypted(total)

    return jsonify({"message": "Aggregation succesfull", "data": serialised_ciphertext}), 200

@main.route('/net_worth', methods=['GET'])
def calculate_net_worth():
    """
    Calculates net worth from the total in aggregation: (Revenue + Savings + Investments) - (Expenses + Loans)
    Returns encrypted results
    Decrypted Print statements are just for checking purposes
    """
    load_secret(encryption_obj)
    # Get all the sum values from /aggregate which returns a ciphertext of total
    try:
        agg_response = aggregation()
        serialised_total = agg_response[0].json['data']
        total_ciphertext = deserialised(serialised_total, encryption_obj)

        if total_ciphertext is None:
            return jsonify({"error": "Failed to deserialize aggregated data"}), 500
        
        # Sum of (Revenue + Savings + Investments)
        positive_sum = total_ciphertext.copy() # Revenue

        # Savings is at index 2
        savings = total_ciphertext.copy()
        savings <<= 2
        positive_sum += savings

        # Investments is at index 3
        investments = total_ciphertext.copy()
        investments <<= 3
        positive_sum += investments

        # Expenses at Index 1
        negative_sum = total_ciphertext.copy() # Currently at Revenue
        negative_sum <<= 1

        # Add Loans
        loans = total_ciphertext.copy()
        loans <<= 4
        negative_sum += loans

        net_worth = sub_encrypted(positive_sum, negative_sum)
        decrypted_net_worth = decrypt_value(encryption_obj, net_worth)
        print(f"Net Worth: {decrypted_net_worth[0]:.2f}")
        serialised_ciphertext = serialised_encrypted(net_worth)

        return jsonify({"message": "Net worth calculation successful", "data": serialised_ciphertext}), 200

    except Exception as e:
        print(f"An error occurred during net worth calculation: {e}")
        return jsonify({"error": "Failed to calculate net worth"}), 500
