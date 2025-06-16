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
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), height_ratios=[3, 1], constrained_layout=True)
            
            # Calculate and plot data
            Income = df[df["Amount"] > 0].resample("D").sum().reindex(df.index, fill_value=0)
            Expense = df[df["Amount"] < 0].resample("D").sum().reindex(df.index, fill_value=0)
            
            # Plot income and expenses
            ax1.plot(Income.index, Income["Amount"], label="Income", color="green", marker='o', markersize=4)
            ax1.plot(Expense.index, abs(Expense["Amount"]), label="Expense", color="red", marker='o', markersize=4)
            
            ax1.set_title('Income and Expenses Over Time', pad=20, fontsize=12)
            ax1.set_xlabel('Date', labelpad=10, fontsize=10)
            ax1.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
            
            # Plot net savings
            net_savings = Income["Amount"] + Expense["Amount"]  # Expense is already negative
            ax2.plot(net_savings.index, net_savings, label="Net Savings", color="blue", marker='o', markersize=4)
            ax2.set_title('Net Savings Over Time', pad=20, fontsize=12)
            ax2.set_xlabel('Date', labelpad=10, fontsize=10)
            ax2.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
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
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), height_ratios=[2, 1], constrained_layout=True)
            
            # Plot stacked bar chart
            x = range(len(monthly_data))
            width = 0.35
            
            ax1.bar(x, monthly_data['Amount'].apply(lambda x: x['Income']), width, label='Income', color='green')
            ax1.bar(x, monthly_data['Amount'].apply(lambda x: x['Expenses']), width, 
                   bottom=monthly_data['Amount'].apply(lambda x: x['Income']), label='Expenses', color='red')
            
            ax1.set_title('Monthly Income and Expenses', pad=20, fontsize=12)
            ax1.set_xlabel('Month', labelpad=10, fontsize=10)
            ax1.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax1.set_xticks(x)
            ax1.set_xticklabels(monthly_data['Month'], rotation=45, ha='right')
            ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Plot line chart of net savings
            net_savings = monthly_data['Amount'].apply(lambda x: x['Total'])
            ax2.plot(x, net_savings, marker='o', color='purple', label='Net Savings')
            ax2.set_title('Monthly Net Savings', pad=20, fontsize=12)
            ax2.set_xlabel('Month', labelpad=10, fontsize=10)
            ax2.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax2.set_xticks(x)
            ax2.set_xticklabels(monthly_data['Month'], rotation=45, ha='right')
            ax2.grid(True, alpha=0.3)
            ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
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
            plt.figure(figsize=(12, 8), constrained_layout=True)
            plt.pie(currency_counts, labels=currency_counts.index, autopct='%1.1f%%', 
                   textprops={'fontsize': 10})
            plt.title('Distribution of Transactions by Currency', pad=20, fontsize=12)
            
            # Add legend outside the pie chart
            plt.legend(currency_counts.index, title="Currencies",
                      loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                      fontsize=10)
            
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
            plt.figure(figsize=(12, 8), constrained_layout=True)
            plt.pie([total_income, total_expenses], 
                   labels=['Income', 'Expenses'],
                   autopct='%1.1f%%',
                   colors=['green', 'red'],
                   textprops={'fontsize': 10})
            plt.title('Income vs Expenses Distribution', pad=20, fontsize=12)
            
            # Add legend outside the pie chart
            plt.legend(['Income', 'Expenses'], title="Categories",
                      loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                      fontsize=10)
            
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
            plt.figure(figsize=(14, 10), constrained_layout=True)
            colors = plt.cm.Pastel1(np.linspace(0, 1, len(use_counts)))
            plt.pie(use_counts, 
                   labels=use_counts.index,
                   autopct='%1.1f%%',
                   colors=colors,
                   startangle=90,
                   textprops={'fontsize': 10})
            plt.title('Distribution of Transactions by Use Case', pad=20, fontsize=12)
            
            # Add legend outside the pie chart
            plt.legend(use_counts.index,
                      title="Use Cases",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1),
                      fontsize=10)
            
            while True:
                save = input("Do you want to save the plot?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/use_cases_distribution.png', bbox_inches='tight', dpi=300)
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

    @classmethod
    def visualize_predictions(self, predictions, r2_scores):
        try:
            if predictions is None:
                return

            # Create figure with three subplots
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 15), height_ratios=[1, 1, 1], constrained_layout=True)
            
            # Plot income predictions
            ax1.plot(predictions['Dates'], predictions['Income'], 'g-', label='Predicted Income')
            ax1.set_title('Predicted Income Over Time', pad=20, fontsize=12)
            ax1.set_xlabel('Date', labelpad=10, fontsize=10)
            ax1.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax1.grid(True, alpha=0.3)
            ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
            
            # Plot expense predictions
            ax2.plot(predictions['Dates'], predictions['Expenses'], 'r-', label='Predicted Expenses')
            ax2.set_title('Predicted Expenses Over Time', pad=20, fontsize=12)
            ax2.set_xlabel('Date', labelpad=10, fontsize=10)
            ax2.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax2.grid(True, alpha=0.3)
            ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
            # Plot net predictions
            ax3.plot(predictions['Dates'], predictions['Net'], 'b-', label='Predicted Net')
            ax3.set_title('Predicted Net Savings Over Time', pad=20, fontsize=12)
            ax3.set_xlabel('Date', labelpad=10, fontsize=10)
            ax3.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax3.grid(True, alpha=0.3)
            ax3.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
            
            # Add R² scores to the plot
            plt.figtext(0.02, 0.02, 
                       f"Model Accuracy (R² scores):\n"
                       f"Income: {r2_scores['Income']:.3f}\n"
                       f"Expenses: {r2_scores['Expenses']:.3f}\n"
                       f"Net: {r2_scores['Net']:.3f}",
                       fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
            
            while True:
                save = input("Do you want to save the prediction plots?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/future_predictions.png', bbox_inches='tight', dpi=300)
                    print("Prediction visualization saved to 'reports/future_predictions.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating prediction visualization: {error}")

    @classmethod
    def visualize_prediction_comparison(self, comparison, error_metrics):
        try:
            if comparison is None:
                return

            # Create figure with three subplots
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 15), height_ratios=[1, 1, 1], constrained_layout=True)
            
            # Plot income comparison
            ax1.plot(comparison['Dates'], comparison['Predicted_Income'], 'g-', label='Predicted Income')
            ax1.plot(comparison['Dates'], comparison['Actual_Income'], 'g--', label='Actual Income')
            ax1.set_title('Income: Predicted vs Actual', pad=20, fontsize=12)
            ax1.set_xlabel('Date', labelpad=10, fontsize=10)
            ax1.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax1.grid(True, alpha=0.3)
            ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
            
            # Plot expense comparison
            ax2.plot(comparison['Dates'], comparison['Predicted_Expenses'], 'r-', label='Predicted Expenses')
            ax2.plot(comparison['Dates'], comparison['Actual_Expenses'], 'r--', label='Actual Expenses')
            ax2.set_title('Expenses: Predicted vs Actual', pad=20, fontsize=12)
            ax2.set_xlabel('Date', labelpad=10, fontsize=10)
            ax2.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax2.grid(True, alpha=0.3)
            ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
            # Plot net comparison
            ax3.plot(comparison['Dates'], comparison['Predicted_Net'], 'b-', label='Predicted Net')
            ax3.plot(comparison['Dates'], comparison['Actual_Net'], 'b--', label='Actual Net')
            ax3.set_title('Net Savings: Predicted vs Actual', pad=20, fontsize=12)
            ax3.set_xlabel('Date', labelpad=10, fontsize=10)
            ax3.set_ylabel('Amount', labelpad=10, fontsize=10)
            ax3.grid(True, alpha=0.3)
            ax3.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
            
            # Add error metrics to the plot
            plt.figtext(0.02, 0.02, 
                       f"Error Metrics:\n"
                       f"Income - MAE: {error_metrics['Income']['MAE']:.2f}, RMSE: {error_metrics['Income']['RMSE']:.2f}\n"
                       f"Expenses - MAE: {error_metrics['Expenses']['MAE']:.2f}, RMSE: {error_metrics['Expenses']['RMSE']:.2f}\n"
                       f"Net - MAE: {error_metrics['Net']['MAE']:.2f}, RMSE: {error_metrics['Net']['RMSE']:.2f}",
                       fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
            
            while True:
                save = input("Do you want to save the comparison plots?(y,n):").lower()
                ans = ["y", "n"]
                if save not in ans:
                    continue
                elif save == "y":
                    if not os.path.exists('reports'):
                        os.makedirs('reports')
                    plt.savefig('reports/prediction_comparison.png', bbox_inches='tight', dpi=300)
                    print("Comparison visualization saved to 'reports/prediction_comparison.png'")
                    break
                elif save == "n":
                    break
                else:
                    break
            
            plt.show()
            plt.close()
            
        except Exception as error:
            print(f"Error creating prediction comparison visualization: {error}")

