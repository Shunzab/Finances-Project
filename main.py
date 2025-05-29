from core import *
import datetime
today = datetime.date.today()
print(f"Today's date is: {today}")

csv_file.get_csv()

def view_data():
    try:
        data = csv_file.get_csv()
        print(data)
    except Exception as error:
        print(f"An error occurred: {error}")


def add_data():
    try:
        date = input("Please enter the date (DD-MM-YYYY): ")
        amount = input("Please enter the amount: ")
        category = input("Please enter the category of the amount: ")
        use = input("Please enter the use of the amount : ")

        csv_file.add_data(date, amount, category, use)

    except Exception as error:
        print(f"An error occurred: {error}")

# def date():



