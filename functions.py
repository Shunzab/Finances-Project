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
            print("=" * 60)
            print(f"{'Date':<12} {'Amount':>10} {'Category':>7} {'Use':<40}")
            print("-" * 60)
            
            for _, row in data.iterrows():
                print(f"{row['Date']:<12} {row['Amount']:>10.2f} {row['Category']:>7} {row['Use']:<40}")
            
            print("=" * 60)
            
    except Exception as error:
        print(f"An error occurred while viewing data: {error}")

def add_data():
    try:
        date_call() # get date
        date = dates

        amount_call() # get amount
        amount = amounts

        category_call()
        category = categories
        
        use = input("Please enter the use of the amount : ")

        csv_file.add_data(date, amount, category, use)

    except Exception as error:
        print(f"An error occurred: {error}")

def date_call(): # date handler
    try:
        global dates
        dates = input("Please enter the date (DD-MM-YYYY): ")

        datetoday = datetime.datetime.strptime(dates, "%d-%m-%Y").date()
        if datetoday > today: # check that date is not in the future
            print("The date cannot be in the future.")
            
            return date_call()
        else:
            pass

    except ValueError as invformat: # invalid date format
        print(f"Invalid date format: {invformat}")
        return date_call()

def amount_call(): # specifying amount
    try:
        global amounts
        amounts = float(input("Please enter the amount: "))

        if amounts <= 0:
            print("Amount must be greater than zero.")
            return amount_call()
        else:
            pass

    except ValueError as invformat: # invalid amount format
        print(f"Invalid amount format: {invformat}")
        return amount_call()
    
def category_call(): # specifying category
    global categories
    categories = input("Please enter Z for income and X for expenditure.")
    dictcat = ['Z', 'X']
    categories = categories.upper()  # Ensure the input is uppercase
    if categories not in dictcat:
        print("Invalid category. Please enter 'Z' for income or 'X' for expenditure.")
        return category_call()
    else:
        pass


