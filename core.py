import pandas as pd
from datetime import datetime
import csv

class csv_file: # A class to handle CSV file operations.
    CSV_FILE = 'data.csv' # csv file is data.csv called through CSV_FILE
    Columns = ['Date', 'Amount', 'Category', 'Use'] # To put categories in csv file
    
    @classmethod
    def get_csv(self):
        # Initialize the CSV file with headers if it does not exist.
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            file = pd.DataFrame(columns=self.Columns)
            file.to_csv(self.CSV_FILE, index=False)

    @classmethod
    def add_data(self, Date, Amount, Category, Use):
        # Add a new row of data to the CSV file.
        newentry = {
            'Date': Date,
            'Amount': Amount,
            'Category': Category,
            'Use': Use
        }
        self.get_csv()
        with open(self.CSV_FILE, 'a', newline='') as csvfile: # opening csv file in append mode.
            writer = csv.DictWriter(csvfile, fieldnames=self.Columns)
            writer.writerow(newentry)
        print(f"Entry Added.")

class log: # A class to handle logging operations.
    @staticmethod
    def log_in():
        # Log ins to finances.
        with open('login.txt', 'a') as login:
            login.write(f"{datetime.now()}\n")

        print(f"Logged in at {datetime.now()}")
        print(f"Last login at : {pd.read_csv('login.txt').tail(1).to_string(index=False)}")

    @staticmethod
    def log_out():
        # Log outs from finances.
        with open('logout.txt', 'a') as logout:
            logout.write(f"{datetime.now()}\n")

        print(f"Logged out at {datetime.now()}")

