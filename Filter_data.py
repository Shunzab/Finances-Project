from core import *
import pandas as pd
from datetime import datetime
import csv

class filter(csv_file):  # Filter data by amount 
    @classmethod
    def filter_by_amount_range(self, min_amount, max_amount):
        # Filter data by amount range
        try:
            df = pd.read_csv(self.CSV_FILE)  
            filtered_data = df[(df['Amount'] >= min_amount) & (df['Amount'] <= max_amount)]
            
            if not filtered_data.empty:
                print("\nFiltered Data by Amount Range:")
                print("=" * 70)
                print(f"{'Date':<12} {'Amount':>10} {'Currency':>10} {'Type':>10} {'Use':<30}")
                print("-" * 70)
                
                for _, row in filtered_data.iterrows():
                    type_str = "Income" if row['Amount'] > 0 else "Expense"
                    print(f"{row['Date']:<12} {row['Amount']:>10.2f} {row['Currency']:>10} {type_str:>10} {row['Use']:<40}")
                
                print("=" * 70)
                return filtered_data
            else:
                print("No data found in the specified amount range.")
                return None
                
        except Exception as e:
            print(f"Error filtering by amount range: {e}")
            return None

    @classmethod
    def filter_data_by_date(self, start_date, end_date): # filter data for a specific period
        try:
            # Standardize input dates
            start_date = csv_file.standardize_date(start_date)
            end_date = csv_file.standardize_date(end_date)
            
            reader = pd.read_csv(self.CSV_FILE) # read the csv file
            reader["Date"] = pd.to_datetime(reader["Date"], format="%d-%m-%Y")

            # Convert the start date to a datetime object
            start_date = datetime.strptime(start_date, "%d-%m-%Y") 
            end_date = datetime.strptime(end_date, "%d-%m-%Y")      

            # Create a boolean mask to filter the data
            comparator = (reader['Date'] >= start_date) & (reader['Date'] <= end_date)
            filtered_data = reader.loc[comparator]

            if filtered_data.empty:
                print("Sorry, no data in this range.")
            else: 
                print("\nFiltered Data Summary:")
                print("=" * 70)
                print(f"{'Date':<12} {'Amount':>10} {'Currency':>10} {'Type':>10} {'Use':<30}")
                print("-" * 70)
                
                #This will iterate through all the rows in the filtered data
                for _, row in filtered_data.iterrows():
                    type_str = "Income" if row['Amount'] > 0 else "Expense"
                    print(f"{row['Date'].strftime('%d-%m-%Y'):<12} {row['Amount']:>10.2f} {row['Currency']:>10} {type_str:>10} {row['Use']:<40}")
                
                print("=" * 70)
                
                total_income = filtered_data[filtered_data["Amount"] > 0]["Amount"].sum()
                total_expense = abs(filtered_data[filtered_data["Amount"] < 0]["Amount"].sum())
                net_savings = total_income - total_expense

                print("\nSummary for Selected Period:")
                print("-" * 50)
                print(f"Total Income:    {total_income:>10.2f}")
                print(f"Total Expenses:  {total_expense:>10.2f}")
                print(f"Net Savings:     {net_savings:>10.2f}")
                print("=" * 50)
        except Exception as e:
            print(f"Error filtering by date range: {e}")
            return None

    @classmethod
    def summary_of_all_data(self):
        try:
            reader = pd.read_csv(self.CSV_FILE)
            reader["Date"] = pd.to_datetime(reader["Date"], format="%d-%m-%Y") # convert the date to a datetime object

            
            total_income = reader[reader["Amount"] > 0]["Amount"].sum()
            total_expense = abs(reader[reader["Amount"] < 0]["Amount"].sum())
            net_savings = total_income - total_expense

            print("\nOverall Financial Summary:")
            print("=" * 60)
            print(f"Total Income:    {total_income:>10.2f}")
            print(f"Total Expenses:  {total_expense:>10.2f}")
            print(f"Net Savings:     {net_savings:>10.2f}")
            print("=" * 60)

            income_count = len(reader[reader["Amount"] > 0])
            expense_count = len(reader[reader["Amount"] < 0])
            print(f"\nTransaction Summary:")
            print("-" * 60)
            print(f"Number of Income Transactions:    {income_count:>5}")
            print(f"Number of Expense Transactions:   {expense_count:>5}")
            print(f"Total Transactions:              {income_count + expense_count:>5}")
            print("=" * 60)

        except Exception as error:
            print(f"An error occurred while calculating summary: {error}")

    @classmethod
    def expenses_by_month(self): # organizes all the expenses by month
        try:
            df = pd.read_csv(self.CSV_FILE) 
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y") 
            
            # Group by month and calculate income/expenses
            df['Month'] = df['Date'].dt.strftime('%B %Y')
            monthly_data = df.groupby('Month').agg({
                'Amount': lambda x: {
                    'Income': x[x > 0].sum(),
                    'Expenses': abs(x[x < 0].sum()),
                    'Total': x.sum()
                }
            }).reset_index()
            
            
            print("\nMonthly Expense Summary:")
            print("=" * 70)
            print(f"{'Month':<20} {'Income':>10} {'Expenses':>10} {'Total':>10} {'Currency':>10}")
            print("-" * 70)
            
            for _, row in monthly_data.iterrows():
                currency = df[df['Month'] == row['Month']]['Currency'].iloc[0] if not df[df['Month'] == row['Month']].empty else 'PKR'
                print(f"{row['Month']:<20} {row['Amount']['Income']:>10.2f} {row['Amount']['Expenses']:>10.2f} {row['Amount']['Total']:>10.2f} {currency:>10}")
            
            print("=" * 70)
            
            # Calculate and display overall totals
            print("\nOverall Totals:")
            print("-" * 50)
            total_income = monthly_data['Amount'].apply(lambda x: x['Income']).sum()
            total_expenses = monthly_data['Amount'].apply(lambda x: x['Expenses']).sum()
            net_savings = total_income - total_expenses

            print(f"Total Income:    {total_income:>10.2f}")
            print(f"Total Expenses:  {total_expenses:>10.2f}")
            print(f"Net Savings:     {net_savings:>10.2f}")
            print("=" * 50)

        except Exception as error:
            print(f"An error occurred while calculating monthly expenses: {error}")
            return None

    @classmethod
    def filter_by_type(self, type_str): # This is the most difficult one to write.
        # Filter data by type (income/expense)
        try:
            df = pd.read_csv(self.CSV_FILE)
            if type_str.lower() == "income":
                filtered_data = df[df['Amount'] > 0]
            elif type_str.lower() == "expense":
                filtered_data = df[df['Amount'] < 0]
            else:
                print("Invalid type. Please use 'income' or 'expense'.")
                return None
            
            if not filtered_data.empty:
                print(f"\nFiltered Data for {type_str.title()}:")
                print("=" * 70)
                print(f"{'Date':<12} {'Amount':>10} {'Currency':>10} {'Type':>10} {'Use':<30}")
                print("-" * 70)
                
                for _, row in filtered_data.iterrows():
                    type_str = "Income" if row['Amount'] > 0 else "Expense"
                    print(f"{row['Date']:<12} {row['Amount']:>10.2f} {row['Currency']:>10} {type_str:>10} {row['Use']:<40}")
                
                print("=" * 70)
                
                # Calculate summary for the type
                total_amount = abs(filtered_data['Amount'].sum())
                transaction_count = len(filtered_data)
                
                print("\nSummary:")
                print("-" * 50)
                print(f"Total Amount:    {total_amount:>10.2f}")
                print(f"Transactions:    {transaction_count:>10}")
                print("=" * 50)
                
                return filtered_data
            else:
                print(f"No {type_str} transactions found.")
                return None
                
        except Exception as e:
            print(f"Error filtering by type: {e}")
            return None




