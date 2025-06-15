import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def make_predictions(df, forecast_periods=30):
    """
    Generate financial predictions for income, expenses, and net balance.
    
    Args:
        df (pd.DataFrame): Input DataFrame with financial data
        forecast_periods (int): Number of days to forecast
        
    Returns:
        pd.DataFrame: Predictions with confidence intervals
    """
    # Prepare data
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].abs()  # Ensure all amounts are positive
    
    # Create daily aggregates
    daily_data = df.groupby(['Date', 'Category']).agg({
        'Amount': 'sum',
        'Description': 'count'
    }).reset_index()
    
    # Create features
    daily_data['Day'] = daily_data['Date'].dt.day
    daily_data['Month'] = daily_data['Date'].dt.month
    daily_data['DayOfWeek'] = daily_data['Date'].dt.dayofweek
    
    # Separate income and expenses
    income_data = daily_data[daily_data['Category'] == 'Income'].copy()
    expenses_data = daily_data[daily_data['Category'] == 'Expense'].copy()
    
    # Prepare features for prediction
    X_income = income_data[['Day', 'Month', 'DayOfWeek']]
    y_income = income_data['Amount']
    X_expenses = expenses_data[['Day', 'Month', 'DayOfWeek']]
    y_expenses = expenses_data['Amount']
    
    # Train models
    income_model = LinearRegression()
    expenses_model = LinearRegression()
    
    if len(X_income) > 0:
        income_model.fit(X_income, y_income)
    if len(X_expenses) > 0:
        expenses_model.fit(X_expenses, y_expenses)
    
    # Generate future dates
    last_date = df['Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_periods)
    
    # Create prediction features
    future_features = pd.DataFrame({
        'Date': future_dates,
        'Day': future_dates.day,
        'Month': future_dates.month,
        'DayOfWeek': future_dates.dayofweek
    })
    
    # Make predictions
    if len(X_income) > 0:
        income_pred = income_model.predict(future_features[['Day', 'Month', 'DayOfWeek']])
    else:
        income_pred = np.zeros(forecast_periods)
        
    if len(X_expenses) > 0:
        expenses_pred = expenses_model.predict(future_features[['Day', 'Month', 'DayOfWeek']])
    else:
        expenses_pred = np.zeros(forecast_periods)
    
    # Calculate confidence intervals
    if len(X_income) > 0:
        income_std = np.std(y_income - income_model.predict(X_income))
        income_ci = 1.96 * income_std * np.sqrt(1 + np.sum((future_features[['Day', 'Month', 'DayOfWeek']] - X_income.mean())**2, axis=1))
    else:
        income_ci = np.zeros(forecast_periods)
        
    if len(X_expenses) > 0:
        expenses_std = np.std(y_expenses - expenses_model.predict(X_expenses))
        expenses_ci = 1.96 * expenses_std * np.sqrt(1 + np.sum((future_features[['Day', 'Month', 'DayOfWeek']] - X_expenses.mean())**2, axis=1))
    else:
        expenses_ci = np.zeros(forecast_periods)
    
    # Create prediction DataFrame
    predictions = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Income': income_pred,
        'Predicted_Expenses': expenses_pred,
        'Income_CI_Lower': income_pred - income_ci,
        'Income_CI_Upper': income_pred + income_ci,
        'Expenses_CI_Lower': expenses_pred - expenses_ci,
        'Expenses_CI_Upper': expenses_pred + expenses_ci
    })
    
    # Calculate net balance predictions
    predictions['Predicted_Net'] = predictions['Predicted_Income'] - predictions['Predicted_Expenses']
    predictions['Net_CI_Lower'] = predictions['Income_CI_Lower'] - predictions['Expenses_CI_Upper']
    predictions['Net_CI_Upper'] = predictions['Income_CI_Upper'] - predictions['Expenses_CI_Lower']
    
    # Calculate trend indicators
    predictions['Income_Trend'] = predictions['Predicted_Income'].pct_change()
    predictions['Expenses_Trend'] = predictions['Predicted_Expenses'].pct_change()
    predictions['Net_Trend'] = predictions['Predicted_Net'].pct_change()
    
    return predictions, income_model, expenses_model, X_income, y_income, X_expenses, y_expenses

def create_forecast_chart(df, predictions):
    """
    Create the income vs expenses forecast chart.
    
    Args:
        df (pd.DataFrame): Historical data
        predictions (pd.DataFrame): Prediction data
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig_forecast = go.Figure()
    
    # Add historical data
    historical_income = df[df['Category'] == 'Income'].groupby('Date')['Amount'].sum()
    historical_expenses = df[df['Category'] == 'Expense'].groupby('Date')['Amount'].sum()
    
    fig_forecast.add_trace(go.Scatter(
        x=historical_income.index,
        y=historical_income.values,
        name='Historical Income',
        line=dict(color='#2ecc71', width=2),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=historical_expenses.index,
        y=historical_expenses.values,
        name='Historical Expenses',
        line=dict(color='#e74c3c', width=2),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    # Add predictions with confidence intervals
    fig_forecast.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Predicted_Income'],
        name='Predicted Income',
        line=dict(color='#2ecc71', width=2, dash='dash'),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Predicted_Expenses'],
        name='Predicted Expenses',
        line=dict(color='#e74c3c', width=2, dash='dash'),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    # Add confidence intervals
    fig_forecast.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Income_CI_Upper'],
        fill=None,
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Income_CI_Lower'],
        fill='tonexty',
        mode='lines',
        line=dict(width=0),
        name='Income Confidence Interval',
        fillcolor='rgba(46, 204, 113, 0.2)'
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Expenses_CI_Upper'],
        fill=None,
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Expenses_CI_Lower'],
        fill='tonexty',
        mode='lines',
        line=dict(width=0),
        name='Expenses Confidence Interval',
        fillcolor='rgba(231, 76, 60, 0.2)'
    ))
    
    # Add trend annotations
    for i in range(len(predictions)):
        if i > 0:
            # Income trend
            if predictions['Income_Trend'].iloc[i] > 0.05:
                fig_forecast.add_annotation(
                    x=predictions['Date'].iloc[i],
                    y=predictions['Predicted_Income'].iloc[i],
                    text="↑",
                    showarrow=False,
                    font=dict(color='#2ecc71', size=16)
                )
            elif predictions['Income_Trend'].iloc[i] < -0.05:
                fig_forecast.add_annotation(
                    x=predictions['Date'].iloc[i],
                    y=predictions['Predicted_Income'].iloc[i],
                    text="↓",
                    showarrow=False,
                    font=dict(color='#2ecc71', size=16)
                )
            
            # Expenses trend
            if predictions['Expenses_Trend'].iloc[i] > 0.05:
                fig_forecast.add_annotation(
                    x=predictions['Date'].iloc[i],
                    y=predictions['Predicted_Expenses'].iloc[i],
                    text="↑",
                    showarrow=False,
                    font=dict(color='#e74c3c', size=16)
                )
            elif predictions['Expenses_Trend'].iloc[i] < -0.05:
                fig_forecast.add_annotation(
                    x=predictions['Date'].iloc[i],
                    y=predictions['Predicted_Expenses'].iloc[i],
                    text="↓",
                    showarrow=False,
                    font=dict(color='#e74c3c', size=16)
                )
    
    fig_forecast.update_layout(
        title='Income and Expenses Forecast',
        xaxis_title='Date',
        yaxis_title='Amount (USD)',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        template='plotly_white',
        height=500
    )
    
    return fig_forecast

def create_net_balance_chart(df, predictions):
    """
    Create the net balance forecast chart.
    
    Args:
        df (pd.DataFrame): Historical data
        predictions (pd.DataFrame): Prediction data
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig_net = go.Figure()
    
    # Add historical net balance
    historical_income = df[df['Category'] == 'Income'].groupby('Date')['Amount'].sum()
    historical_expenses = df[df['Category'] == 'Expense'].groupby('Date')['Amount'].sum()
    historical_net = historical_income - historical_expenses
    
    fig_net.add_trace(go.Scatter(
        x=historical_net.index,
        y=historical_net.values,
        name='Historical Net Balance',
        line=dict(color='#3498db', width=2),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    # Add predicted net balance
    fig_net.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Predicted_Net'],
        name='Predicted Net Balance',
        line=dict(color='#3498db', width=2, dash='dash'),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    # Add confidence interval
    fig_net.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Net_CI_Upper'],
        fill=None,
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig_net.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Net_CI_Lower'],
        fill='tonexty',
        mode='lines',
        line=dict(width=0),
        name='Confidence Interval',
        fillcolor='rgba(52, 152, 219, 0.2)'
    ))
    
    # Add trend annotations
    for i in range(len(predictions)):
        if i > 0:
            if predictions['Net_Trend'].iloc[i] > 0.05:
                fig_net.add_annotation(
                    x=predictions['Date'].iloc[i],
                    y=predictions['Predicted_Net'].iloc[i],
                    text="↑",
                    showarrow=False,
                    font=dict(color='#3498db', size=16)
                )
            elif predictions['Net_Trend'].iloc[i] < -0.05:
                fig_net.add_annotation(
                    x=predictions['Date'].iloc[i],
                    y=predictions['Predicted_Net'].iloc[i],
                    text="↓",
                    showarrow=False,
                    font=dict(color='#3498db', size=16)
                )
    
    fig_net.update_layout(
        title='Net Balance Forecast',
        xaxis_title='Date',
        yaxis_title='Amount (USD)',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        template='plotly_white',
        height=500
    )
    
    return fig_net

def calculate_prediction_metrics(income_model, expenses_model, X_income, y_income, X_expenses, y_expenses):
    """
    Calculate prediction accuracy metrics.
    
    Args:
        income_model: Trained income prediction model
        expenses_model: Trained expenses prediction model
        X_income: Income features
        y_income: Income target
        X_expenses: Expenses features
        y_expenses: Expenses target
        
    Returns:
        dict: Dictionary containing prediction metrics
    """
    metrics = {}
    
    # Calculate R-squared for income
    if len(X_income) > 0:
        metrics['income_r2'] = income_model.score(X_income, y_income)
        metrics['income_mae'] = np.mean(np.abs(y_income - income_model.predict(X_income)))
    
    # Calculate R-squared for expenses
    if len(X_expenses) > 0:
        metrics['expenses_r2'] = expenses_model.score(X_expenses, y_expenses)
        metrics['expenses_mae'] = np.mean(np.abs(y_expenses - expenses_model.predict(X_expenses)))
    
    return metrics 