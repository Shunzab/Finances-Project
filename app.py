import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import io
import base64
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from predictions import make_predictions, create_forecast_chart, create_net_balance_chart, calculate_prediction_metrics

# Set page configuration
st.set_page_config(
    page_title="Financial Management System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("💰 Financial Management System")
st.markdown("Track and analyze your financial transactions with ease.")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv')
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Function to download data
def get_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to create gauge chart
def create_gauge_chart(value, title, min_val, max_val):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [min_val, max_val/3], 'color': "lightgray"},
                {'range': [max_val/3, 2*max_val/3], 'color': "gray"},
                {'range': [2*max_val/3, max_val], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val*0.8
            }
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# Load the data
df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Category filter
    all_categories = ['All'] + sorted(df['Use'].unique().tolist())
    selected_category = st.sidebar.selectbox("Select Category", all_categories)
    
    # Currency filter
    all_currencies = ['All'] + sorted(df['Currency'].unique().tolist())
    selected_currency = st.sidebar.selectbox("Select Currency", all_currencies)

    # Amount range filter
    min_amount = df['Amount'].min()
    max_amount = df['Amount'].max()
    amount_range = st.sidebar.slider(
        "Amount Range",
        min_value=float(min_amount),
        max_value=float(max_amount),
        value=(float(min_amount), float(max_amount))
    )
    
    # Apply filters
    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= date_range[0]) &
            (filtered_df['Date'].dt.date <= date_range[1])
        ]
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Use'] == selected_category]
    if selected_currency != 'All':
        filtered_df = filtered_df[filtered_df['Currency'] == selected_currency]
    filtered_df = filtered_df[
        (filtered_df['Amount'] >= amount_range[0]) &
        (filtered_df['Amount'] <= amount_range[1])
    ]

    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    total_income = filtered_df[filtered_df['Amount'] > 0]['Amount'].sum()
    total_expenses = abs(filtered_df[filtered_df['Amount'] < 0]['Amount'].sum())
    net_balance = total_income - total_expenses
    avg_transaction = filtered_df['Amount'].mean()
    
    # Display metrics with improved styling
    with col1:
        st.metric("Total Income", f"${total_income:,.2f}", delta=f"{((total_income/5000)-1)*100:.1f}%")
    with col2:
        st.metric("Total Expenses", f"${total_expenses:,.2f}", delta=f"{((total_expenses/5000)-1)*100:.1f}%")
    with col3:
        st.metric("Net Balance", f"${net_balance:,.2f}", delta=f"{((net_balance/5000)-1)*100:.1f}%")
    with col4:
        st.metric("Avg Transaction", f"${avg_transaction:,.2f}")

    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Trends", "📝 Transactions", "📤 Export", "🔮 Predictions"])

    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Expense by category pie chart with improved styling
            st.subheader("Expenses by Category")
            expense_df = filtered_df[filtered_df['Amount'] < 0].copy()
            expense_df['Amount'] = abs(expense_df['Amount'])
            
            # Calculate percentages for labels
            total_exp = expense_df['Amount'].sum()
            expense_df['Percentage'] = (expense_df['Amount'] / total_exp * 100).round(1)
            
            fig_pie = px.pie(
                expense_df,
                values='Amount',
                names='Use',
                title='Expense Distribution by Category',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            # Update layout for better visualization
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=12,
                marker=dict(line=dict(color='#000000', width=1))
            )
            
            fig_pie.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                title_x=0.5,
                title_font_size=20
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Income vs Expenses bar chart with improved styling
            st.subheader("Income vs Expenses by Category")
            income_df = filtered_df[filtered_df['Amount'] > 0].groupby('Use')['Amount'].sum().reset_index()
            expense_df = filtered_df[filtered_df['Amount'] < 0].groupby('Use')['Amount'].sum().reset_index()
            expense_df['Amount'] = abs(expense_df['Amount'])
            
            # Create the bar chart with improved styling
            fig_bar = go.Figure()
            
            # Add income bars
            fig_bar.add_trace(go.Bar(
                x=income_df['Use'],
                y=income_df['Amount'],
                name='Income',
                marker_color='#2ecc71',
                marker_line_color='#27ae60',
                marker_line_width=1.5,
                opacity=0.8
            ))
            
            # Add expense bars
            fig_bar.add_trace(go.Bar(
                x=expense_df['Use'],
                y=expense_df['Amount'],
                name='Expenses',
                marker_color='#e74c3c',
                marker_line_color='#c0392b',
                marker_line_width=1.5,
                opacity=0.8
            ))
            
            # Update layout for better visualization
            fig_bar.update_layout(
                title='Income vs Expenses by Category',
                barmode='group',
                xaxis_title='Category',
                yaxis_title='Amount ($)',
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                plot_bgcolor='white',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray',
                    tickangle=45
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                title_x=0.5,
                title_font_size=20
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Time series analysis with improved styling
            st.subheader("Income vs Expenses Over Time")
            
            # Prepare data for time series
            daily_data = filtered_df.groupby('Date').agg({
                'Amount': lambda x: sum(x[x > 0]),  # Income
                'Amount': lambda x: sum(x[x < 0])   # Expenses
            }).reset_index()
            
            daily_data.columns = ['Date', 'Income', 'Expenses']
            daily_data['Expenses'] = abs(daily_data['Expenses'])
            
            # Create line chart with improved styling
            fig_line = go.Figure()
            
            # Add income line
            fig_line.add_trace(go.Scatter(
                x=daily_data['Date'],
                y=daily_data['Income'],
                name='Income',
                line=dict(color='#2ecc71', width=3),
                mode='lines+markers',
                marker=dict(size=8)
            ))
            
            # Add expense line
            fig_line.add_trace(go.Scatter(
                x=daily_data['Date'],
                y=daily_data['Expenses'],
                name='Expenses',
                line=dict(color='#e74c3c', width=3),
                mode='lines+markers',
                marker=dict(size=8)
            ))
            
            # Update layout for better visualization
            fig_line.update_layout(
                title='Income vs Expenses Over Time',
                xaxis_title='Date',
                yaxis_title='Amount ($)',
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                plot_bgcolor='white',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                title_x=0.5,
                title_font_size=20
            )
            
            st.plotly_chart(fig_line, use_container_width=True)

        with col2:
            # Monthly trend with improved styling
            st.subheader("Monthly Trend")
            monthly_data = filtered_df.copy()
            monthly_data['Month'] = monthly_data['Date'].dt.strftime('%Y-%m')
            monthly_summary = monthly_data.groupby('Month').agg({
                'Amount': lambda x: sum(x[x > 0]),  # Income
                'Amount': lambda x: sum(x[x < 0])   # Expenses
            }).reset_index()
            monthly_summary.columns = ['Month', 'Income', 'Expenses']
            monthly_summary['Expenses'] = abs(monthly_summary['Expenses'])
            monthly_summary['Net'] = monthly_summary['Income'] - monthly_summary['Expenses']
            
            # Create bar chart with improved styling
            fig_monthly = go.Figure()
            
            # Add net balance bars
            fig_monthly.add_trace(go.Bar(
                x=monthly_summary['Month'],
                y=monthly_summary['Net'],
                name='Net Balance',
                marker_color='#3498db',
                marker_line_color='#2980b9',
                marker_line_width=1.5,
                opacity=0.8
            ))
            
            # Update layout for better visualization
            fig_monthly.update_layout(
                title='Monthly Net Balance',
                xaxis_title='Month',
                yaxis_title='Amount ($)',
                showlegend=True,
                plot_bgcolor='white',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray',
                    tickangle=45
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                title_x=0.5,
                title_font_size=20
            )
            
            st.plotly_chart(fig_monthly, use_container_width=True)

            # Add gauge chart for savings rate
            st.subheader("Savings Rate")
            savings_rate = (net_balance / total_income * 100) if total_income > 0 else 0
            gauge_fig = create_gauge_chart(
                savings_rate,
                "Monthly Savings Rate (%)",
                0,
                100
            )
            st.plotly_chart(gauge_fig, use_container_width=True)

    with tab3:
        # Transaction list with search and sort
        st.subheader("Transaction History")
        
        # Search functionality
        search_term = st.text_input("Search transactions", "")
        
        # Format the dataframe for display
        display_df = filtered_df.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%d-%m-%Y')
        display_df['Amount'] = display_df['Amount'].map('${:,.2f}'.format)
        
        # Apply search filter
        if search_term:
            display_df = display_df[
                display_df['Use'].str.contains(search_term, case=False) |
                display_df['Comment'].str.contains(search_term, case=False)
            ]
        
        # Reorder columns for better display
        display_df = display_df[['Date', 'Amount', 'Currency', 'Use', 'Comment']]
        
        # Display with sorting capability and improved styling
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with tab4:
        st.subheader("Export Data")
        
        # Export options
        export_format = st.radio("Select export format", ["CSV", "Excel"])
        
        if export_format == "CSV":
            st.markdown(get_download_link(filtered_df, "financial_data.csv", "Download CSV"), unsafe_allow_html=True)
        else:
            # Excel export
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, sheet_name='Financial Data', index=False)
            buffer.seek(0)
            st.download_button(
                label="Download Excel",
                data=buffer,
                file_name="financial_data.xlsx",
                mime="application/vnd.ms-excel"
            )
        
        # Summary statistics with improved styling
        st.subheader("Summary Statistics")
        stats_df = filtered_df.describe()
        st.dataframe(
            stats_df,
            use_container_width=True,
            height=300
        )

    with tab5:
        st.header("🔮 Financial Predictions")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            forecast_periods = st.slider("Forecast Period (Days)", 7, 90, 30)
            confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
        
        with col2:
            st.metric("Prediction Horizon", f"{forecast_periods} days")
            st.metric("Confidence Interval", f"±{(100-confidence_level)/2}%")
        
        # Make predictions
        predictions, income_model, expenses_model, X_income, y_income, X_expenses, y_expenses = make_predictions(filtered_df, forecast_periods)
        
        # Income vs Expenses Forecast
        st.subheader("Income vs Expenses Forecast")
        fig_forecast = create_forecast_chart(filtered_df, predictions)
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Net Balance Forecast
        st.subheader("Net Balance Forecast")
        fig_net = create_net_balance_chart(filtered_df, predictions)
        st.plotly_chart(fig_net, use_container_width=True)
        
        # Prediction Summary
        st.subheader("Prediction Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_income = predictions['Predicted_Income'].mean()
            current_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].mean()
            income_change = ((avg_income - current_income) / current_income * 100) if current_income != 0 else 0
            st.metric(
                "Average Predicted Income",
                f"${avg_income:,.2f}",
                f"{income_change:+.1f}%"
            )
        
        with col2:
            avg_expenses = predictions['Predicted_Expenses'].mean()
            current_expenses = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].mean()
            expenses_change = ((avg_expenses - current_expenses) / current_expenses * 100) if current_expenses != 0 else 0
            st.metric(
                "Average Predicted Expenses",
                f"${avg_expenses:,.2f}",
                f"{expenses_change:+.1f}%"
            )
        
        with col3:
            avg_net = predictions['Predicted_Net'].mean()
            current_net = (filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum() - 
                          filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum())
            net_change = ((avg_net - current_net) / abs(current_net) * 100) if current_net != 0 else 0
            st.metric(
                "Average Predicted Net Balance",
                f"${avg_net:,.2f}",
                f"{net_change:+.1f}%"
            )
        
        # Prediction Accuracy Metrics
        st.subheader("Prediction Accuracy")
        col1, col2 = st.columns(2)
        
        metrics = calculate_prediction_metrics(income_model, expenses_model, X_income, y_income, X_expenses, y_expenses)
        
        with col1:
            if 'income_r2' in metrics:
                st.metric("Income Prediction R²", f"{metrics['income_r2']:.2%}")
            if 'expenses_r2' in metrics:
                st.metric("Expenses Prediction R²", f"{metrics['expenses_r2']:.2%}")
        
        with col2:
            if 'income_mae' in metrics:
                st.metric("Income MAE", f"${metrics['income_mae']:,.2f}")
            if 'expenses_mae' in metrics:
                st.metric("Expenses MAE", f"${metrics['expenses_mae']:,.2f}")

else:
    st.error("Please ensure your data file (data.csv) is in the correct format and location.") 