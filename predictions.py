from core import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

class predictions(csv_file):
    @classmethod
    def prepare_data(self):
        try:
            # Read and prepare data
            df = pd.read_csv(self.CSV_FILE)
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            df = df.sort_values("Date")
            
            # Create daily aggregates
            daily_data = df.groupby('Date').agg({
                'Amount': lambda x: {
                    'Income': x[x > 0].sum(),
                    'Expenses': abs(x[x < 0].sum()),
                    'Net': x.sum()
                }
            }).reset_index()
            
            # Create features for prediction
            daily_data['Days'] = (daily_data['Date'] - daily_data['Date'].min()).dt.days
            
            return daily_data
        except Exception as e:
            print(f"Error preparing data: {e}")
            return None

    @classmethod
    def predict_future(self, days_to_predict=30):
        try:
            daily_data = self.prepare_data()
            if daily_data is None:
                return None

            # Prepare features for prediction
            X = daily_data['Days'].values.reshape(-1, 1)
            y_income = daily_data['Amount'].apply(lambda x: x['Income']).values
            y_expenses = daily_data['Amount'].apply(lambda x: x['Expenses']).values
            y_net = daily_data['Amount'].apply(lambda x: x['Net']).values

            # Create polynomial features
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)

            # Train models
            models = {
                'Income': LinearRegression(),
                'Expenses': LinearRegression(),
                'Net': LinearRegression()
            }

            models['Income'].fit(X_poly, y_income)
            models['Expenses'].fit(X_poly, y_expenses)
            models['Net'].fit(X_poly, y_net)

            # Generate future dates
            last_date = daily_data['Date'].max()
            future_dates = [last_date + timedelta(days=x) for x in range(1, days_to_predict + 1)]
            future_days = np.array([(date - daily_data['Date'].min()).days for date in future_dates]).reshape(-1, 1)
            future_days_poly = poly.transform(future_days)

            # Make predictions
            predictions = {
                'Dates': future_dates,
                'Income': models['Income'].predict(future_days_poly),
                'Expenses': models['Expenses'].predict(future_days_poly),
                'Net': models['Net'].predict(future_days_poly)
            }

            # Calculate R² scores
            r2_scores = {
                'Income': r2_score(y_income, models['Income'].predict(X_poly)),
                'Expenses': r2_score(y_expenses, models['Expenses'].predict(X_poly)),
                'Net': r2_score(y_net, models['Net'].predict(X_poly))
            }

            return predictions, r2_scores

        except Exception as e:
            print(f"Error making predictions: {e}")
            return None

    @classmethod
    def get_prediction_summary(self, predictions, r2_scores):
        try:
            if predictions is None:
                return

            print("\nPrediction Summary:")
            print("=" * 60)
            print(f"Prediction Period: {predictions['Dates'][0].strftime('%d-%m-%Y')} to {predictions['Dates'][-1].strftime('%d-%m-%Y')}")
            print("-" * 60)
            
            # Calculate averages
            avg_income = np.mean(predictions['Income'])
            avg_expenses = np.mean(predictions['Expenses'])
            avg_net = np.mean(predictions['Net'])
            
            print(f"Predicted Average Income:    {avg_income:>10.2f}")
            print(f"Predicted Average Expenses:  {avg_expenses:>10.2f}")
            print(f"Predicted Average Net:       {avg_net:>10.2f}")
            print("-" * 60)
            
            # Display R² scores
            print("\nModel Accuracy (R² scores):")
            print(f"Income Prediction:   {r2_scores['Income']:.3f}")
            print(f"Expenses Prediction: {r2_scores['Expenses']:.3f}")
            print(f"Net Prediction:      {r2_scores['Net']:.3f}")
            print("=" * 60)
            
            # Add confidence warning
            print("\nNote: Predictions are based on historical data and may not reflect future trends.")
            print("Higher R² scores indicate more reliable predictions.")

        except Exception as e:
            print(f"Error generating prediction summary: {e}")

    @classmethod
    def compare_predictions_with_actual(self, days_to_compare=30):
        try:
            # Get predictions for the past period
            predictions_data, r2_scores = self.predict_future(days_to_compare)
            if predictions_data is None:
                return None

            # Get actual data for the same period
            df = pd.read_csv(self.CSV_FILE)
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            
            # Filter data for the prediction period
            start_date = predictions_data['Dates'][0]
            end_date = predictions_data['Dates'][-1]
            mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
            actual_data = df[mask]

            # Aggregate actual data by date
            actual_daily = actual_data.groupby('Date').agg({
                'Amount': lambda x: {
                    'Income': x[x > 0].sum(),
                    'Expenses': abs(x[x < 0].sum()),
                    'Net': x.sum()
                }
            }).reset_index()

            # Calculate differences
            comparison = {
                'Dates': predictions_data['Dates'],
                'Predicted_Income': predictions_data['Income'],
                'Actual_Income': [0] * len(predictions_data['Dates']),
                'Predicted_Expenses': predictions_data['Expenses'],
                'Actual_Expenses': [0] * len(predictions_data['Dates']),
                'Predicted_Net': predictions_data['Net'],
                'Actual_Net': [0] * len(predictions_data['Dates'])
            }

            # Fill in actual values where available
            for date in actual_daily['Date']:
                idx = predictions_data['Dates'].index(date)
                actual_values = actual_daily[actual_daily['Date'] == date]['Amount'].iloc[0]
                comparison['Actual_Income'][idx] = actual_values['Income']
                comparison['Actual_Expenses'][idx] = actual_values['Expenses']
                comparison['Actual_Net'][idx] = actual_values['Net']

            # Calculate error metrics
            error_metrics = {
                'Income': {
                    'MAE': np.mean(np.abs(np.array(comparison['Predicted_Income']) - np.array(comparison['Actual_Income']))),
                    'RMSE': np.sqrt(np.mean((np.array(comparison['Predicted_Income']) - np.array(comparison['Actual_Income']))**2))
                },
                'Expenses': {
                    'MAE': np.mean(np.abs(np.array(comparison['Predicted_Expenses']) - np.array(comparison['Actual_Expenses']))),
                    'RMSE': np.sqrt(np.mean((np.array(comparison['Predicted_Expenses']) - np.array(comparison['Actual_Expenses']))**2))
                },
                'Net': {
                    'MAE': np.mean(np.abs(np.array(comparison['Predicted_Net']) - np.array(comparison['Actual_Net']))),
                    'RMSE': np.sqrt(np.mean((np.array(comparison['Predicted_Net']) - np.array(comparison['Actual_Net']))**2))
                }
            }

            return comparison, error_metrics

        except Exception as e:
            print(f"Error comparing predictions with actual data: {e}")
            return None

    @classmethod
    def get_comparison_summary(self, comparison, error_metrics):
        try:
            if comparison is None:
                return

            print("\nPrediction vs Actual Comparison Summary:")
            print("=" * 80)
            print(f"Comparison Period: {comparison['Dates'][0].strftime('%d-%m-%Y')} to {comparison['Dates'][-1].strftime('%d-%m-%Y')}")
            print("-" * 80)
            
            # Calculate averages
            print("\nAverage Values:")
            print(f"{'Metric':<15} {'Predicted':>15} {'Actual':>15} {'Difference':>15}")
            print("-" * 80)
            
            for metric in ['Income', 'Expenses', 'Net']:
                pred_avg = np.mean(comparison[f'Predicted_{metric}'])
                actual_avg = np.mean(comparison[f'Actual_{metric}'])
                diff = pred_avg - actual_avg
                print(f"{metric:<15} {pred_avg:>15.2f} {actual_avg:>15.2f} {diff:>15.2f}")
            
            print("\nError Metrics:")
            print(f"{'Metric':<15} {'MAE':>15} {'RMSE':>15}")
            print("-" * 80)
            
            for metric in ['Income', 'Expenses', 'Net']:
                print(f"{metric:<15} {error_metrics[metric]['MAE']:>15.2f} {error_metrics[metric]['RMSE']:>15.2f}")
            
            print("=" * 80)
            print("\nNote: MAE (Mean Absolute Error) and RMSE (Root Mean Square Error) indicate prediction accuracy.")
            print("Lower values indicate better predictions.")

        except Exception as e:
            print(f"Error generating comparison summary: {e}") 