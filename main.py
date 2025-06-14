from core import * # wildcard import all the functions from the core module
import datetime
from functions import * # wildcard import all the functions from the functions module
today = datetime.date.today()


def main():
    # Print the current date
    print(f"\nToday's date is: {today}")

    # Print the menu and iterates through the menu until the user exits.
    while True:
        print("\nMenu:")
        # Print the options
        print("1. View Data")
        print("2. Add Data")
        print("3. Exit")
        
        choice = input("Please select an option (1-3): ")
        
        if choice == '1':
            view_data() # view the data
        elif choice == '2':
            add_data() # add data
        elif choice == '3':
            print("Exiting the program.") # exit the program
            break
        else:
            print("Invalid choice, please try again.")

main()
