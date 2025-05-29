from core import *
import datetime
from functions import view_data, add_data
today = datetime.date.today()


def main():
    print(f"Today's date is: {today}")
    while True:
        print("\nMenu:")
        print("1. View Data")
        print("2. Add Data")
        print("3. Exit")
        
        choice = input("Please select an option (1-3): ")
        
        if choice == '1':
            view_data()
        elif choice == '2':
            add_data()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")