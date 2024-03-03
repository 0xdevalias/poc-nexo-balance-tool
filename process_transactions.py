#!/usr/bin/env python

# from decimal import Decimal

import pandas as pd

def add_to_balance(balances, currency, amount):
    balances[currency] = balances.get(currency, 0) + amount

def subtract_from_balance(balances, currency, amount):
    balances[currency] = balances.get(currency, 0) - amount

def process_transactions(csv_path):
    df = pd.read_csv(csv_path)
    main_balances = {}

    simple_add_types = ['Top up Crypto', 'Referral Bonus', 'Exchange Cashback', 'Dividend', 'Interest']

    for index, row in df.iterrows():
        transaction_type = row['Type']
        input_currency = row['Input Currency']
        output_currency = row['Output Currency']
        output_amount = row['Output Amount']
        input_amount = row['Input Amount']

        transaction_date = pd.to_datetime(row['Date / Time (UTC)'])

        if transaction_type in simple_add_types:
            if input_currency in ['USD', 'DAI']:
                add_to_balance(main_balances, 'DAI', input_amount)
            else:
                add_to_balance(main_balances, output_currency, output_amount)
        elif transaction_type == 'Withdrawal':
            subtract_from_balance(main_balances, output_currency, output_amount)
        elif transaction_type == 'Exchange':
            subtract_from_balance(main_balances, input_currency, abs(input_amount))
            add_to_balance(main_balances, output_currency, output_amount)
        elif transaction_type == 'Transfer To Pro Wallet':
            subtract_from_balance(main_balances, output_currency, output_amount)
        elif transaction_type == 'Transfer From Pro Wallet':
            add_to_balance(main_balances, output_currency, output_amount)

    # return pd.Series(main_balances).sort_index()[pd.Series(main_balances).sort_index() != 0]
    return pd.Series(main_balances).sort_index()

if __name__ == '__main__':
    csv_path = '/Users/devalias/Desktop/20240303 - Nexo_Transactions_1709443516.csv'  # Update this path to your CSV file location
    final_balances = process_transactions(csv_path)

    # Iterating through the Series to print each item without exponential notation
    for currency, balance in final_balances.items():
        print(f"{currency}: {balance:.8f}")
    # print()

    # # Iterating through the Series to print each item with full precision
    # for currency, balance in final_balances.items():
    #     print(f"{currency}: {str(balance)}")
    # print()

    # # Iterating through the Series to print each item with full precision, avoiding exponential notation
    # for currency, balance in final_balances.items():
    #     # Convert the balance to Decimal for exact arithmetic
    #     decimal_balance = Decimal(balance)
    #     # Format the Decimal as a string without exponential notation
    #     formatted_balance = format(decimal_balance, 'f')
    #     print(f"{currency}: {formatted_balance}")
    # print()
