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
            
            # Print the filtered data in a readable format
            if not filtered_data.empty:
                print("\nFiltered Data by Amount Range:")
                print("=" * 50)
                print(f"{'Date':<12} {'Amount':>10} {'Category':>10} {'Use':<30}")
                print("-" * 50)
                
                for _, row in filtered_data.iterrows():
                    print(f"{row['Date']:<12} {row['Amount']:>10.2f} {row['Category']:>7} {row['Use']:<40}")
                
                print("=" * 50)
                return filtered_data
            else:
                print("No data found in the specified amount range.")
                return None
                
        except Exception as e:
            print(f"Error filtering by amount range: {e}")
            return None

    @classmethod
    def filter_data_by_date(self, start_date, end_date): # filter data for a specific period
        reader = pd.read_csv(self.CSV_FILE) # read the csv file
        reader["Date"] = pd.to_datetime(reader["Date"], format="%d-%m-%Y")

        # Convert the start date to a datetime object
        start_date = datetime.strptime(start_date,"%d-%m-%Y") 
        end_date = datetime.strptime(end_date,"%d-%m-%Y")      

        # Create a boolean mask to filter the data
        comparator = (reader['Date'] >= start_date) & (reader['Date'] <= end_date)
        filtered_data = reader.loc[comparator]

        if filtered_data.empty:
            print("Sorry, no data in this range.")
        else: # making the data appear in a preety way
            print("\nFiltered Data Summary:")
            print("=" * 50)
            print(f"{'Date':<12} {'Amount':>10} {'Category':>10} {'Use':<30}")
            print("-" * 50)
            
            #This will iterate through all the rows in the filtered data
            for _, row in filtered_data.iterrows():
                print(f"{row['Date'].strftime('%d-%m-%Y'):<12} {row['Amount']:>10.2f} {row['Category']:>7} {row['Use']:<40}")
            
            print("=" * 50)
            
            # Calculate summary
            total_income = filtered_data[filtered_data["Category"] == "Z"]["Amount"].sum()
            total_expense = filtered_data[filtered_data["Category"] == "X"]["Amount"].sum()
            net_savings = total_income - total_expense

            # Print Summary
            print("\nSummary for Selected Period:")
            print("-" * 50)
            print(f"Total Income:    {total_income:>10.2f}")
            print(f"Total Expenses:  {total_expense:>10.2f}")
            print(f"Net Savings:     {net_savings:>10.2f}")
            print("=" * 50)


    @classmethod
    def summary_of_all_data(self):
        try:
            reader = pd.read_csv(self.CSV_FILE) # read the csv file
            reader["Date"] = pd.to_datetime(reader["Date"], format="%d-%m-%Y") # convert the date to a datetime object

            # Calculate totals
            total_income = reader[reader["Category"] == "Z"]["Amount"].sum()
            total_expense = reader[reader["Category"] == "X"]["Amount"].sum()
            net_savings = total_income - total_expense

            # Display summary
            print("\nOverall Financial Summary:")
            print("=" * 60)
            print(f"Total Income:    {total_income:>10.2f}")
            print(f"Total Expenses:  {total_expense:>10.2f}")
            print(f"Net Savings:     {net_savings:>10.2f}")
            print("=" * 60)

            # Display transaction counts
            income_count = len(reader[reader["Category"] == "Z"])
            expense_count = len(reader[reader["Category"] == "X"])
            print(f"\nTransaction Summary:")
            print("-" * 60)
            print(f"Number of Income Transactions:    {income_count:>5}")
            print(f"Number of Expense Transactions:   {expense_count:>5}")
            print(f"Total Transactions:              {income_count + expense_count:>5}")
            print("=" * 60)

        except Exception as error:
            print(f"An error occurred while calculating summary: {error}")

    @classmethod
    def expenses_by_month(self): # organizes all the expencses by month
        try:
            df = pd.read_csv(self.CSV_FILE) # read the csv file
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y") # convert the date to a datetime object
            
            # Group by month and category
            df['Month'] = df['Date'].dt.strftime('%B %Y')
            monthly_summary = df.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
            
            # Calculate totals for each month
            monthly_summary['Total'] = monthly_summary.sum(axis=1)
            
            # Format the output
            print("\nMonthly Expense Summary:")
            print("=" * 60)
            print(f"{'Month':<20} {'Income':>10} {'Expenses':>10} {'Total':>10}")
            print("-" * 60)
            
            for month in monthly_summary.index: # iterate through all the months
                income = monthly_summary.loc[month, 'Z'] if 'Z' in monthly_summary.columns else 0
                expenses = monthly_summary.loc[month, 'X'] if 'X' in monthly_summary.columns else 0
                total = monthly_summary.loc[month, 'Total']
                print(f"{month:<20} {income:>10.2f} {expenses:>10.2f} {total:>10.2f}")
            
            print("=" * 60)
            
            # Calculate and display overall totals
            print("\nOverall Totals:")
            print("-" * 50)
            total_income = monthly_summary['Z'].sum() if 'Z' in monthly_summary.columns else 0
            total_expenses = monthly_summary['X'].sum() if 'X' in monthly_summary.columns else 0
            net_savings = total_income - total_expenses

            print(f"Total Income:    {total_income:>10.2f}")
            print(f"Total Expenses:  {total_expenses:>10.2f}")
            print(f"Net Savings:     {net_savings:>10.2f}")
            print("=" * 50)

        except Exception as error:
            print(f"An error occurred while calculating monthly expenses: {error}")
            return None

    @classmethod
    def filter_by_category(self, category):
        # Filter data by category
        try:
            df = pd.read_csv(self.CSV_FILE)
            filtered_data = df[df['Category'] == category]
            
            if not filtered_data.empty:
                print(f"\nFiltered Data for Category {category}:")
                print("=" * 50)
                print(f"{'Date':<12} {'Amount':>10} {'Category':>10} {'Use':<30}")
                print("-" * 50)
                
                for _, row in filtered_data.iterrows():
                    print(f"{row['Date']:<12} {row['Amount']:>10.2f} {row['Category']:>7} {row['Use']:<40}")
                
                print("=" * 50)
                
                # Calculate summary for the category
                total_amount = filtered_data['Amount'].sum()
                transaction_count = len(filtered_data)
                
                print("\nCategory Summary:")
                print("-" * 50)
                print(f"Total Amount:    {total_amount:>10.2f}")
                print(f"Transactions:    {transaction_count:>10}")
                print("=" * 50)
                
                return filtered_data
            else:
                print(f"No data found for category {category}")
                return None
                
        except Exception as e:
            print(f"Error filtering by category: {e}")
            return None




