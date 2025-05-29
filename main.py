from core import *
import datetime
today = datetime.date.today()
print(f"Today's date is: {today}")



def view_data():
    try:
        csv_file.get_csv()
        data =pd.read_csv(csv_file.CSV_FILE)
        if data.empty:
            print("No data available.")
        else:
            print("Current data in the CSV file:")
            print(data)
    except Exception as error:
        print(f"An error occurred while viewing data: {error}")

def add_data():
    try:
        date = date_call()
        amount = input("Please enter the amount: ")
        category = input("Please enter the category of the amount: ")
        use = input("Please enter the use of the amount : ")

        csv_file.add_data(date, amount, category, use)

    except Exception as error:
        print(f"An error occurred: {error}")

def date_call():
    try:
        date = input("Please enter the date (DD-MM-YYYY): ")

        datetoday = datetime.datetime.strptime(date, "%d-%m-%Y").date()
        if datetoday > today: # check that date is not in the future
            print("The date cannot be in the future.")
            
            return date_call()
        else:
            pass

    except ValueError as invformat: # invalid date format
        print(f"Invalid date format: {invformat}")
        return date_call()

view_data()