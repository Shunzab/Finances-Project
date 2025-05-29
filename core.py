import pandas as pd
import datetime as dt
import csv

class csv_file: # A class to handle CSV file operations.
    CSV_FILE = 'data.csv'
    Columns = ['Date', 'Amount', 'Category', 'Use']
    
    @classmethod
    def get_csv(self):
        # Initialize the CSV file with headers if it does not exist.
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            file = pd.DataFrame(columns=self.Columns)
            file.to_csv(self.CSV_FILE, index=False)

    @classmethod
    def add_data(self, date, amount, category, use):
        # Add a new row of data to the CSV file.
        newentry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Use': use
        }
        self.get_csv()
        with open(self.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.Columns)
            writer.writerow(newentry)
        print(f"Added entry: {newentry}")

class log: # A class to handle logging operations.
    @staticmethod
    def log_in():
        # Log ins to finances.
        with open('login.txt', 'a') as login:
            login.write(f"{dt.datetime.now()}\n")

        print(f"Logged in at {dt.datetime.now()}")
        print(f'Last login at : {pd.read_txt('login.txt').tail(1).to_string(index=False)}')

    @staticmethod
    def log_out():
        # Log outs from finances.
        with open('logout.txt', 'a') as logout:
            logout.write(f"{dt.datetime.now()}\n")

        print(f"Logged out at {dt.datetime.now()}")