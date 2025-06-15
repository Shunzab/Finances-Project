from core import *
import pandas as pd
import datetime
today = datetime.date.today()

def view_data():
    try:
        csv_file.get_csv() # get the csv file
        data = pd.read_csv(csv_file.CSV_FILE)
        if data.empty:
            print("No data available.")
        else:
            print("\nCurrent Data Summary:")
            print("=" * 100)
            print(f"{'Date':<12} {'Amount':>10} {'Currency':>10} {'Type':>10} {'Use':<30} {'Comment':<30}")
            print("-" * 100)
            
            for _, row in data.iterrows():
                type_str = "Income" if row['Amount'] > 0 else "Expense"
                print(f"{row['Date']:<12} {row['Amount']:>10.2f} {row['Currency']:>10} {type_str:>10} {row['Use']:<30} {row['Comment']:<30}")
            
            print("=" * 100)
            
            # Calculate and display summary
            total_income = data[data["Amount"] > 0]["Amount"].sum()
            total_expense = abs(data[data["Amount"] < 0]["Amount"].sum())
            net_savings = total_income - total_expense
            
            print("\nSummary:")
            print("-" * 50)
            print(f"Total Income:    {total_income:>10.2f}")
            print(f"Total Expenses:  {total_expense:>10.2f}")
            print(f"Net Savings:     {net_savings:>10.2f}")
            print("=" * 50)
            
    except Exception as error:
        print(f"An error occurred while viewing data: {error}")

def add_data():
    try:
        date_call() # get date
        date = dates

        amount_call() # get amount
        amount = amounts

        Currency_call()
        Currency = currencies

        Use = input('What is the use/origin of this amount: ')
        if not Use:
            print("Use/origin cannot be empty.")
            return add_data()
        
        Comment = input("Any Comments (press Enter to skip): ").strip()
        if not Comment:
            Comment = "No comment"

        # Determine if it's income or expense
        transaction_type = input("Is this an income or expense? (i/e): ").lower().strip()
        if transaction_type == 'e':
            amount = -abs(amount)  # Make sure expense is negative
        elif transaction_type == 'i':
            amount = abs(amount)   # Make sure income is positive
        else:
            print("Invalid transaction type. Please use 'i' for income or 'e' for expense.")
            return add_data()

        csv_file.add_data(date, amount, Currency, Use, Comment)
        print("\nData added successfully!")

    except Exception as error:
        print(f"An error occurred: {error}")

def date_call(): # date handler
    try:
        global dates
        dates = input("Please enter the date (DD-MM-YYYY): ")

        # Validate date format
        try:
            datetoday = datetime.datetime.strptime(dates, "%d-%m-%Y").date()
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY format.")
            return date_call()

        if datetoday > today: # check that date is not in the future
            print("The date cannot be in the future.")
            return date_call()
        
        return dates

    except Exception as error:
        print(f"Error in date input: {error}")
        return date_call()

def amount_call(): # specifying amount
    try:
        global amounts
        amount_str = input("Please enter the amount: ").strip()
        
        try:
            amounts = float(amount_str)
        except ValueError:
            print("Invalid amount format. Please enter a valid number.")
            return amount_call()

        if amounts == 0:
            print("Amount cannot be zero.")
            return amount_call()
        
        return amounts

    except Exception as error:
        print(f"Error in amount input: {error}")
        return amount_call()
    
def Currency_call(): # specifying Currency
    try:
        global currencies
        global default_currency
        default_currency = 'PKR'
        
        currencies = ""

        while True:
            ask_currency = input("Do You want to go with the default currency(PKR), or use another currency?(y/n):").lower().strip()
            if ask_currency == 'y':
                currencies = input('Please enter the currency:').strip().upper()
                if not currencies:
                    print("Currency cannot be empty. Using default currency (PKR).")
                    currencies = default_currency
                break
            elif ask_currency == 'n':
                currencies = default_currency
                break
            else:
                print('Please enter a valid value(y/n).')
                continue
        
        return currencies

    except Exception as error:
        print(f"Error in currency input: {error}")
        return default_currency

def delete_transaction():
    try:
        csv_file.get_csv()
        data = pd.read_csv(csv_file.CSV_FILE)
        
        if data.empty:
            print("No data available to delete.")
            return
        
        # Display current data
        print("\nCurrent Transactions:")
        print("=" * 100)
        print(f"{'Index':<6} {'Date':<12} {'Amount':>10} {'Currency':>10} {'Type':>10} {'Use':<30}")
        print("-" * 100)
        
        for idx, row in data.iterrows():
            type_str = "Income" if row['Amount'] > 0 else "Expense"
            print(f"{idx:<6} {row['Date']:<12} {row['Amount']:>10.2f} {row['Currency']:>10} {type_str:>10} {row['Use']:<30}")
        
        print("=" * 100)
        
        # Get index to delete
        while True:
            try:
                idx = int(input("\nEnter the index of the transaction to delete (or -1 to cancel): "))
                if idx == -1:
                    print("Deletion cancelled.")
                    return
                if idx < 0 or idx >= len(data):
                    print("Invalid index. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
                continue
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete transaction {idx}? (y/n): ").lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return
        
        # Delete the transaction
        data = data.drop(idx)
        data.to_csv(csv_file.CSV_FILE, index=False)
        print("Transaction deleted successfully!")
        
    except Exception as error:
        print(f"An error occurred while deleting transaction: {error}")

def edit_transaction():
    try:
        csv_file.get_csv()
        data = pd.read_csv(csv_file.CSV_FILE)
        
        if data.empty:
            print("No data available to edit.")
            return
        
        # Display current data
        print("\nCurrent Transactions:")
        print("=" * 100)
        print(f"{'Index':<6} {'Date':<12} {'Amount':>10} {'Currency':>10} {'Type':>10} {'Use':<30}")
        print("-" * 100)
        
        for idx, row in data.iterrows():
            type_str = "Income" if row['Amount'] > 0 else "Expense"
            print(f"{idx:<6} {row['Date']:<12} {row['Amount']:>10.2f} {row['Currency']:>10} {type_str:>10} {row['Use']:<30}")
        
        print("=" * 100)
        
        # Get index to edit
        while True:
            try:
                idx = int(input("\nEnter the index of the transaction to edit (or -1 to cancel): "))
                if idx == -1:
                    print("Edit cancelled.")
                    return
                if idx < 0 or idx >= len(data):
                    print("Invalid index. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
                continue
        
        # Get new values
        print("\nEnter new values (press Enter to keep current value):")
        
        # Date
        new_date = input(f"Date [{data.iloc[idx]['Date']}]: ").strip()
        if not new_date:
            new_date = data.iloc[idx]['Date']
        else:
            try:
                new_date = csv_file.standardize_date(new_date)
            except ValueError as e:
                print(f"Invalid date format. {str(e)}")
                print("Keeping current date.")
                new_date = data.iloc[idx]['Date']
        
        # Amount
        new_amount = input(f"Amount [{data.iloc[idx]['Amount']}]: ").strip()
        if not new_amount:
            new_amount = data.iloc[idx]['Amount']
        else:
            try:
                new_amount = float(new_amount)
                # Keep the sign based on transaction type
                if new_amount != 0:
                    transaction_type = input("Is this an income or expense? (i/e): ").lower().strip()
                    if transaction_type == 'e':
                        new_amount = -abs(new_amount)
                    elif transaction_type == 'i':
                        new_amount = abs(new_amount)
                    else:
                        print("Invalid transaction type. Keeping current value.")
                        new_amount = data.iloc[idx]['Amount']
            except ValueError:
                print("Invalid amount format. Keeping current value.")
                new_amount = data.iloc[idx]['Amount']
        
        # Currency
        new_currency = input(f"Currency [{data.iloc[idx]['Currency']}]: ").strip().upper()
        if not new_currency:
            new_currency = data.iloc[idx]['Currency']
        
        # Use
        new_use = input(f"Use [{data.iloc[idx]['Use']}]: ").strip()
        if not new_use:
            new_use = data.iloc[idx]['Use']
        
        # Comment
        new_comment = input(f"Comment [{data.iloc[idx]['Comment']}]: ").strip()
        if not new_comment:
            new_comment = data.iloc[idx]['Comment']
        
        # Update the transaction
        data.iloc[idx] = [new_date, new_amount, new_currency, new_use, new_comment]
        data.to_csv(csv_file.CSV_FILE, index=False)
        print("Transaction updated successfully!")
        
    except Exception as error:
        print(f"An error occurred while editing transaction: {error}")

