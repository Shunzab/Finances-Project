from core import *
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from Filter_data import filter
import os

class graphing(csv_file):
    @classmethod
    def visualize_all_data(self):
        try:
            # Read and prepare data
            df = pd.read_csv(self.CSV_FILE)
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            df.set_index("Date", inplace=True)
            
            # Create figure first
            plt.figure(figsize=(12, 6))
            
            # Calculate and plot data
            Income = df[df["Category"] == "Z"].resample("D").sum().reindex(df.index, fill_value=0)
            Expense = df[df["Category"] == "X"].resample("D").sum().reindex(df.index, fill_value=0)
            
            plt.plot(Income.index, Income["Amount"], label="Income", color="b")
            plt.plot(Expense.index, Expense["Amount"], label="Expense", color="r")
            
            plt.title('Income and Expenses')
            plt.xlabel('Date')
            plt.ylabel('Amount')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/trends_over_time.png', bbox_inches='tight', dpi=300)
                    print("Trend visualization saved to 'reports/trends_over_time.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating visualization: {error}")

    @classmethod
    def visualize_monthly_trends(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            
            # T am creating date into date-time object to get help in plot
            df['Month'] = df['Date'].dt.strftime('%B %Y')
            monthly_data = df.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
            
            # Sort the index by date
            monthly_data.index = pd.to_datetime(monthly_data.index, format='%B %Y')
            monthly_data = monthly_data.sort_index()
            monthly_data.index = monthly_data.index.strftime('%B %Y')
            
        
            monthly_data.plot(kind='bar', stacked=True)
            plt.title('Monthly Income and Expenses')
            plt.xlabel('Month')
            plt.ylabel('Amount')
            plt.xticks(rotation=45)
            plt.legend(['Expenses', 'Income'])
            plt.tight_layout()
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/monthly_trends.png', bbox_inches='tight', dpi=300)
                    print("Monthly trends visualization saved to 'reports/monthly_trends.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating visualization: {error}")


