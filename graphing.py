from core import *
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from Filter_data import filter
import os
import numpy as np

class graphing(csv_file):
    @classmethod
    def visualize_all_data(self):
        try:
            # Read and prepare data
            df = pd.read_csv(self.CSV_FILE)
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            df = df.sort_values("Date")  # Sort by date
            df.set_index("Date", inplace=True)
            
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
            
            # Calculate and plot data
            Income = df[df["Amount"] > 0].resample("D").sum().reindex(df.index, fill_value=0)
            Expense = df[df["Amount"] < 0].resample("D").sum().reindex(df.index, fill_value=0)
            
            # Plot income and expenses
            ax1.plot(Income.index, Income["Amount"], label="Income", color="green", marker='o', markersize=4)
            ax1.plot(Expense.index, abs(Expense["Amount"]), label="Expense", color="red", marker='o', markersize=4)
            
            ax1.set_title('Income and Expenses Over Time')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Amount')
            ax1.legend()
            ax1.grid(True)
            
            # Plot net savings
            net_savings = Income["Amount"] + Expense["Amount"]  # Expense is already negative
            ax2.plot(net_savings.index, net_savings, label="Net Savings", color="blue", marker='o', markersize=4)
            ax2.set_title('Net Savings Over Time')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Amount')
            ax2.legend()
            ax2.grid(True)
            
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
            
            # Create date into date-time object to get help in plot
            df['Month'] = df['Date'].dt.strftime('%B %Y')
            
            # Calculate monthly totals
            monthly_data = df.groupby('Month').agg({
                'Amount': lambda x: {
                    'Income': x[x > 0].sum(),
                    'Expenses': abs(x[x < 0].sum()),
                    'Total': x.sum()
                }
            }).reset_index()
            
            # Sort the data by date
            monthly_data['Date'] = pd.to_datetime(monthly_data['Month'], format='%B %Y')
            monthly_data = monthly_data.sort_values('Date')
            monthly_data['Month'] = monthly_data['Date'].dt.strftime('%B %Y')
            
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[2, 1])
            
            # Plot stacked bar chart
            x = range(len(monthly_data))
            width = 0.35
            
            ax1.bar(x, monthly_data['Amount'].apply(lambda x: x['Income']), width, label='Income', color='green')
            ax1.bar(x, monthly_data['Amount'].apply(lambda x: x['Expenses']), width, bottom=monthly_data['Amount'].apply(lambda x: x['Income']), label='Expenses', color='red')
            
            ax1.set_title('Monthly Income and Expenses')
            ax1.set_xlabel('Month')
            ax1.set_ylabel('Amount')
            ax1.set_xticks(x)
            ax1.set_xticklabels(monthly_data['Month'], rotation=45)
            ax1.legend()
            
            # Plot line chart of net savings
            net_savings = monthly_data['Amount'].apply(lambda x: x['Total'])
            ax2.plot(x, net_savings, marker='o', color='purple', label='Net Savings')
            ax2.set_title('Monthly Net Savings')
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Amount')
            ax2.set_xticks(x)
            ax2.set_xticklabels(monthly_data['Month'], rotation=45)
            ax2.grid(True)
            ax2.legend()
            
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

    @classmethod
    def visualize_currency_distribution(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            
            # Count transactions by currency and sort by count
            currency_counts = df['Currency'].value_counts().sort_values(ascending=False)
            
            # Create pie chart
            plt.figure(figsize=(10, 6))
            plt.pie(currency_counts, labels=currency_counts.index, autopct='%1.1f%%')
            plt.title('Distribution of Transactions by Currency')
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/currency_distribution.png', bbox_inches='tight', dpi=300)
                    print("Currency distribution visualization saved to 'reports/currency_distribution.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating currency distribution visualization: {error}")

    @classmethod
    def visualize_income_expense_ratio(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            
            # Calculate total income and expenses
            total_income = df[df['Amount'] > 0]['Amount'].sum()
            total_expenses = abs(df[df['Amount'] < 0]['Amount'].sum())
            
            # Create pie chart
            plt.figure(figsize=(10, 6))
            plt.pie([total_income, total_expenses], 
                   labels=['Income', 'Expenses'],
                   autopct='%1.1f%%',
                   colors=['green', 'red'])
            plt.title('Income vs Expenses Distribution')
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/income_expense_ratio.png', bbox_inches='tight', dpi=300)
                    print("Income vs Expenses ratio visualization saved to 'reports/income_expense_ratio.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating income vs expenses ratio visualization: {error}")

    @classmethod
    def visualize_use_cases(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            
            # Count transactions by use case and sort by count
            use_counts = df['Use'].value_counts().sort_values(ascending=False)
            
            # If there are too many use cases, combine the smaller ones into "Others"
            if len(use_counts) > 10:
                # Keep top 9 use cases and combine the rest
                top_uses = use_counts.head(9)
                other_uses = use_counts[9:].sum()
                use_counts = pd.concat([top_uses, pd.Series({'Others': other_uses})])
            
            # Create pie chart
            plt.figure(figsize=(12, 8))
            colors = plt.cm.Pastel1(np.linspace(0, 1, len(use_counts)))
            plt.pie(use_counts, 
                   labels=use_counts.index,
                   autopct='%1.1f%%',
                   colors=colors,
                   startangle=90)
            plt.title('Distribution of Transactions by Use Case')
            
            # Add a legend
            plt.legend(use_counts.index,
                      title="Use Cases",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.tight_layout()
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/use_cases_distribution.png', 
                              bbox_inches='tight', 
                              dpi=300)
                    print("Use cases distribution visualization saved to 'reports/use_cases_distribution.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating use cases visualization: {error}")

    @classmethod
    def visualize_use_cases_by_type(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            
            # Create separate pie charts for income and expenses
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            
            # Income use cases - sort by count
            income_uses = df[df['Amount'] > 0]['Use'].value_counts().sort_values(ascending=False)
            if len(income_uses) > 5:
                top_income = income_uses.head(4)
                other_income = income_uses[4:].sum()
                income_uses = pd.concat([top_income, pd.Series({'Others': other_income})])
            
            # Expense use cases - sort by count
            expense_uses = df[df['Amount'] < 0]['Use'].value_counts().sort_values(ascending=False)
            if len(expense_uses) > 5:
                top_expense = expense_uses.head(4)
                other_expense = expense_uses[4:].sum()
                expense_uses = pd.concat([top_expense, pd.Series({'Others': other_expense})])
            
            # Plot income use cases
            colors1 = plt.cm.Greens(np.linspace(0.3, 0.8, len(income_uses)))
            ax1.pie(income_uses, 
                   labels=income_uses.index,
                   autopct='%1.1f%%',
                   colors=colors1,
                   startangle=90)
            ax1.set_title('Income Use Cases')
            
            # Plot expense use cases
            colors2 = plt.cm.Reds(np.linspace(0.3, 0.8, len(expense_uses)))
            ax2.pie(expense_uses, 
                   labels=expense_uses.index,
                   autopct='%1.1f%%',
                   colors=colors2,
                   startangle=90)
            ax2.set_title('Expense Use Cases')
            
            plt.suptitle('Distribution of Use Cases by Transaction Type', y=1.05)
            plt.tight_layout()
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/use_cases_by_type.png', 
                              bbox_inches='tight', 
                              dpi=300)
                    print("Use cases by type visualization saved to 'reports/use_cases_by_type.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating use cases by type visualization: {error}")

