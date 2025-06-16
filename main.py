from core import * # wildcard import all the functions from the core module
from datetime import datetime
from functions import * 
from Filter_data import *
from graphing import *
from predictions import *
import matplotlib.pyplot as plt
from logs import *
from users import *
import os
import csv

today = datetime.today()

def clear_screen(): # i just learnt it right now and it makes things pretty
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n=== Financial Management System ===")
    print("1. View All Transactions")
    print("2. Add New Transaction")
    print("3. Delete Transaction")
    print("4. Edit Transaction")
    print("\n=== Filtering Options ===")
    print("5. Filter by Amount Range")
    print("6. Filter by Date Range")
    print("7. Filter by Type (Income/Expense)")
    print("8. View Monthly Summary")
    print("9. View Overall Summary")
    print("\n=== Visualization Options ===")
    print("10. View Income/Expense Trends")
    print("11. View Monthly Trends")
    print("12. View Currency Distribution")
    print("13. View Income vs Expenses Ratio")
    print("14. View Use Cases Distribution")
    print("15. View Use Cases by Type (Income/Expenses)")
    print("\n=== Prediction Options ===")
    print("16. View Future Predictions")
    print("17. View Prediction Summary")
    print("18. Compare Predictions with Actual Data")
    print("19. View Prediction Comparison Summary")
    print("\n=== Exit ===")
    print("0. Exit Program")

def get_amount_range():
    while True:
        try:
            min_amount = float(input("Enter minimum amount: "))
            max_amount = float(input("Enter maximum amount: "))
            if min_amount > max_amount:
                print("Minimum amount cannot be greater than maximum amount.")
                continue
            return min_amount, max_amount
        except ValueError:
            print("Please enter valid numbers.")

def get_date_range():
    while True:
        try:
            start_date = input("Enter start date (DD-MM-YYYY): ")
            end_date = input("Enter end date (DD-MM-YYYY): ")
            # Validate date format
            datetime.strptime(start_date, "%d-%m-%Y")
            datetime.strptime(end_date, "%d-%m-%Y")
            return start_date, end_date
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY format.")

def main():
    while True:
        clear_screen()
        display_menu()
        
        try:
            choice = input("\nEnter your choice (0-19): ").strip()
            
            if choice == "0":
                print("\nThank you for using the Financial Management System!")
                break
                
            elif choice == "1":
                view_data()
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                add_data()
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                delete_transaction()
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                edit_transaction()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                print("\nFilter by Amount Range")
                min_amount, max_amount = get_amount_range()
                filter.filter_by_amount_range(min_amount, max_amount)
                input("\nPress Enter to continue...")
                
            elif choice == "6":
                print("\nFilter by Date Range")
                start_date, end_date = get_date_range()
                filter.filter_data_by_date(start_date, end_date)
                input("\nPress Enter to continue...")
                
            elif choice == "7":
                print("\nFilter by Type")
                while True:
                    type_choice = input("Enter type (income/expense): ").lower().strip()
                    if type_choice in ["income", "expense"]:
                        filter.filter_by_type(type_choice)
                        break
                    else:
                        print("Invalid type. Please enter 'income' or 'expense'.")
                input("\nPress Enter to continue...")
                
            elif choice == "8":
                print("\nMonthly Summary")
                filter.expenses_by_month()
                input("\nPress Enter to continue...")
                
            elif choice == "9":
                print("\nOverall Summary")
                filter.summary_of_all_data()
                input("\nPress Enter to continue...")
                
            elif choice == "10":
                print("\nGenerating Income/Expense Trends...")
                graphing.visualize_all_data()
                input("\nPress Enter to continue...")
                
            elif choice == "11":
                print("\nGenerating Monthly Trends...")
                graphing.visualize_monthly_trends()
                input("\nPress Enter to continue...")
                
            elif choice == "12":
                print("\nGenerating Currency Distribution...")
                graphing.visualize_currency_distribution()
                input("\nPress Enter to continue...")
                
            elif choice == "13":
                print("\nGenerating Income vs Expenses Ratio...")
                graphing.visualize_income_expense_ratio()
                input("\nPress Enter to continue...")
                
            elif choice == "14":
                print("\nGenerating Use Cases Distribution...")
                graphing.visualize_use_cases()
                input("\nPress Enter to continue...")
                
            elif choice == "15":
                print("\nGenerating Use Cases by Type (Income/Expenses)...")
                graphing.visualize_use_cases_by_type()
                input("\nPress Enter to continue...")
                
            elif choice == "16":
                print("\nGenerating Future Predictions...")
                try:
                    days = int(input("Enter number of days to predict (default: 30): ") or "30")
                    predictions_data, r2_scores = predictions.predict_future(days)
                    if predictions_data:
                        graphing.visualize_predictions(predictions_data, r2_scores)
                except ValueError:
                    print("Invalid input. Using default 30 days.")
                    predictions_data, r2_scores = predictions.predict_future()
                    if predictions_data:
                        graphing.visualize_predictions(predictions_data, r2_scores)
                input("\nPress Enter to continue...")
                
            elif choice == "17":
                print("\nGenerating Prediction Summary...")
                try:
                    days = int(input("Enter number of days to predict (default: 30): ") or "30")
                    predictions_data, r2_scores = predictions.predict_future(days)
                    if predictions_data:
                        predictions.get_prediction_summary(predictions_data, r2_scores)
                except ValueError:
                    print("Invalid input. Using default 30 days.")
                    predictions_data, r2_scores = predictions.predict_future()
                    if predictions_data:
                        predictions.get_prediction_summary(predictions_data, r2_scores)
                input("\nPress Enter to continue...")
                
            elif choice == "18":
                print("\nComparing Predictions with Actual Data...")
                try:
                    days = int(input("Enter number of days to compare (default: 30): ") or "30")
                    comparison_data, error_metrics = predictions.compare_predictions_with_actual(days)
                    if comparison_data:
                        graphing.visualize_prediction_comparison(comparison_data, error_metrics)
                except ValueError:
                    print("Invalid input. Using default 30 days.")
                    comparison_data, error_metrics = predictions.compare_predictions_with_actual()
                    if comparison_data:
                        graphing.visualize_prediction_comparison(comparison_data, error_metrics)
                input("\nPress Enter to continue...")
                
            elif choice == "19":
                print("\nGenerating Prediction Comparison Summary...")
                try:
                    days = int(input("Enter number of days to compare (default: 30): ") or "30")
                    comparison_data, error_metrics = predictions.compare_predictions_with_actual(days)
                    if comparison_data:
                        predictions.get_comparison_summary(comparison_data, error_metrics)
                except ValueError:
                    print("Invalid input. Using default 30 days.")
                    comparison_data, error_metrics = predictions.compare_predictions_with_actual()
                    if comparison_data:
                        predictions.get_comparison_summary(comparison_data, error_metrics)
                input("\nPress Enter to continue...")
                
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")
                
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("\nPress Enter to continue...")


main()