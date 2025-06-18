import pandas as pd
from datetime import datetime
import csv

class csv_file: # A class to handle CSV file operations.
    CSV_FILE = 'data.csv' # csv file is data.csv called through CSV_FILE
    Columns = ['Date', 'Amount', 'Currency', 'Use', 'Comment'] # To put categories in csv file
    
    @classmethod
    def standardize_date(self, date_str):
        try:
            # Try different common date formats
            formats = [
                "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d",
                "%d-%m-%y", "%d/%m/%y", "%y-%m-%d", "%y/%m/%d",
                "%d.%m.%Y", "%d.%m.%y", "%Y.%m.%d", "%y.%m.%d"
            ]
            
            # Try each format
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return date_obj.strftime("%d-%m-%Y")
                except ValueError:
                    continue
            
            raise ValueError(f"Unable to parse date: {date_str}")
        except Exception as e:
            raise ValueError(f"Date standardization error: {str(e)}")

    @classmethod
    def get_csv(self):
        # Initialize the CSV file with headers if it does not exist.
        try:
            df = pd.read_csv(self.CSV_FILE)
            # Standardize dates in existing data
            if not df.empty:
                df['Date'] = df['Date'].apply(self.standardize_date)
                df.to_csv(self.CSV_FILE, index=False)
            return df
        except FileNotFoundError:
            file = pd.DataFrame(columns=self.Columns)
            file.to_csv(self.CSV_FILE, index=False)
            
            with open(self.CSV_FILE, 'a', newline='') as csvfile: # opening csv file in append mode.
                writer = csv.DictWriter(csvfile, fieldnames=self.Columns)
                sample_dict = {
                'Date': '01-01-2025',
                'Amount': 1,
                'Currency': 'PKR',
                'Use': 'Error Handling',
                'Comment':'This will be added if file is not present to avoid errors. This sample entry will be automatically deleted upon your first entry.'
                }
                writer.writerow(sample_dict)
                return file

    @classmethod
    def add_data(self, Date, Amount, Currency, Use, Comment):
        # Add a new row of data to the CSV file.
        try:
            # Standardize the date format
            standardized_date = self.standardize_date(Date)
            
            newentry = {
                'Date': standardized_date,
                'Amount': Amount,
                'Currency': Currency,
                'Use': Use,
                'Comment': Comment
            }
            

            df = self.get_csv()
            
            # sample data removal
            if len(df) == 1 and df.iloc[0]['Use'] == 'Error Handling' and df.iloc[0]['Comment'] == 'This will be added if file is not present to avoid errors. This sample entry will be automatically deleted upon your first entry.':
                
                df = df.drop(0)
                df.to_csv(self.CSV_FILE, index=False)
            
            # Add the new entry
            with open(self.CSV_FILE, 'a', newline='') as csvfile: # opening csv file in append mode.
                writer = csv.DictWriter(csvfile, fieldnames=self.Columns)
                writer.writerow(newentry)
            print(f"Entry Added.")
        except Exception as e:
            print(f"Error adding data: {str(e)}")


