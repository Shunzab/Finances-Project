import streamlit as st
from functions import *
from Filter_data import *
from graphing import *
from predictions import *

st.set_page_config(page_title="Financial Management System", layout="wide")

st.title("💸 Financial Management System")

menu = [
    "View All Transactions", "Add New Transaction", "Delete Transaction", "Edit Transaction",
    "Filter by Amount Range", "Filter by Date Range", "Filter by Type",
    "Monthly Summary", "Overall Summary",
    "Income/Expense Trends", "Monthly Trends", "Currency Distribution",
    "Income vs Expenses Ratio", "Use Cases Distribution", "Use Cases by Type",
    "Future Predictions", "Prediction Summary", "Compare Predictions", "Prediction Comparison Summary"
]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View All Transactions":
    st.subheader("All Transactions")
    # You can use st.dataframe() to show a DataFrame
    df = csv_file.get_csv()
    st.dataframe(df)

elif choice == "Add New Transaction":
    st.subheader("Add Transaction")
    with st.form("add_form"):
        date = st.date_input("Date")
        amount = st.number_input("Amount", step=0.01)
        currency = st.text_input("Currency", value="PKR")
        use = st.text_input("Use/Origin")
        comment = st.text_input("Comment")
        transaction_type = st.radio("Type", ["Income", "Expense"])
        submitted = st.form_submit_button("Add")
        if submitted:
            amt = amount if transaction_type == "Income" else -abs(amount)
            csv_file.add_data(date.strftime("%d-%m-%Y"), amt, currency, use, comment)
            st.success("Transaction added!")

elif choice == "Delete Transaction":
    st.subheader("Delete Transaction")
    df = csv_file.get_csv()
    st.dataframe(df)
    idx = st.number_input("Index to delete", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Delete"):
        df = df.drop(idx)
        df.to_csv(csv_file.CSV_FILE, index=False)
        st.success("Transaction deleted!")

elif choice == "Edit Transaction":
    st.subheader("Edit Transaction")
    df = csv_file.get_csv()
    st.dataframe(df)
    idx = st.number_input("Index to edit", min_value=0, max_value=len(df)-1, step=1)
    row = df.iloc[idx]
    with st.form("edit_form"):
        date = st.date_input("Date", value=row['Date'])
        amount = st.number_input("Amount", value=float(row['Amount']))
        currency = st.text_input("Currency", value=row['Currency'])
        use = st.text_input("Use/Origin", value=row['Use'])
        comment = st.text_input("Comment", value=row['Comment'])
        transaction_type = st.radio("Type", ["Income", "Expense"], index=0 if row['Amount'] > 0 else 1)
        submitted = st.form_submit_button("Update")
        if submitted:
            amt = amount if transaction_type == "Income" else -abs(amount)
            df.at[idx, 'Date'] = date.strftime("%d-%m-%Y")
            df.at[idx, 'Amount'] = amt
            df.at[idx, 'Currency'] = currency
            df.at[idx, 'Use'] = use
            df.at[idx, 'Comment'] = comment
            df.to_csv(csv_file.CSV_FILE, index=False)
            st.success("Transaction updated!")

elif choice == "Filter by Amount Range":
    st.subheader("Filter by Amount Range")
    min_amt = st.number_input("Min Amount")
    max_amt = st.number_input("Max Amount")
    if st.button("Filter"):
        filtered = filter.filter_by_amount_range(min_amt, max_amt)
        if filtered is not None:
            st.dataframe(filtered)

elif choice == "Filter by Date Range":
    st.subheader("Filter by Date Range")
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    if st.button("Filter"):
        filter.filter_data_by_date(start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y"))

elif choice == "Filter by Type":
    st.subheader("Filter by Type")
    t = st.radio("Type", ["Income", "Expense"])
    if st.button("Filter"):
        filter.filter_by_type(t.lower())

elif choice == "Monthly Summary":
    st.subheader("Monthly Summary")
    filter.expenses_by_month()

elif choice == "Overall Summary":
    st.subheader("Overall Summary")
    filter.summary_of_all_data()

elif choice == "Income/Expense Trends":
    st.subheader("Income/Expense Trends")
    graphing.visualize_all_data()

elif choice == "Monthly Trends":
    st.subheader("Monthly Trends")
    graphing.visualize_monthly_trends()

elif choice == "Currency Distribution":
    st.subheader("Currency Distribution")
    graphing.visualize_currency_distribution()

elif choice == "Income vs Expenses Ratio":
    st.subheader("Income vs Expenses Ratio")
    graphing.visualize_income_expense_ratio()

elif choice == "Use Cases Distribution":
    st.subheader("Use Cases Distribution")
    graphing.visualize_use_cases()

elif choice == "Use Cases by Type":
    st.subheader("Use Cases by Type")
    graphing.visualize_use_cases_by_type()

elif choice == "Future Predictions":
    st.subheader("Future Predictions")
    days = st.number_input("Days to predict", min_value=1, value=30)
    predictions_data, r2_scores = predictions.predict_future(days)
    if predictions_data:
        graphing.visualize_predictions(predictions_data, r2_scores)

elif choice == "Prediction Summary":
    st.subheader("Prediction Summary")
    days = st.number_input("Days to predict", min_value=1, value=30)
    predictions_data, r2_scores = predictions.predict_future(days)
    if predictions_data:
        predictions.get_prediction_summary(predictions_data, r2_scores)

elif choice == "Compare Predictions":
    st.subheader("Compare Predictions with Actual Data")
    days = st.number_input("Days to compare", min_value=1, value=30)
    comparison_data, error_metrics = predictions.compare_predictions_with_actual(days)
    if comparison_data:
        graphing.visualize_prediction_comparison(comparison_data, error_metrics)

elif choice == "Prediction Comparison Summary":
    st.subheader("Prediction Comparison Summary")
    days = st.number_input("Days to compare", min_value=1, value=30)
    comparison_data, error_metrics = predictions.compare_predictions_with_actual(days)
    if comparison_data:
        predictions.get_comparison_summary(comparison_data, error_metrics)