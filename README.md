# Financial Management System

A comprehensive command-line based financial management system that helps users track, analyze, and predict their financial transactions with powerful visualization capabilities.

## Features

### Transaction Management
- View all transactions
- Add new transactions
- Delete existing transactions
- Edit transaction details
- Support for multiple currencies

### Data Filtering
- Filter by amount range
- Filter by date range
- Filter by transaction type (Income/Expense)
- View monthly summaries
- View overall financial summary

### Visualization
- Income/Expense trends
- Monthly trends analysis
- Currency distribution charts
- Income vs Expenses ratio visualization
- Use cases distribution
- Use cases by type (Income/Expenses)

### Predictive Analytics
- Future financial predictions
- Prediction summaries
- Comparison of predictions with actual data
- Prediction accuracy metrics

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/Shunzab/Finances-Project]
cd [Finances-Project]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- streamlit==1.31.1
- pandas==2.2.0
- plotly==5.18.0
- xlsxwriter==3.1.9
- scikit-learn==1.4.0
- statsmodels==0.14.1
- numpy==1.26.3
- matplotlib

## Usage

1. Run the main program:
```bash
python main.py
```

2. Follow the interactive menu to:
   - Manage your transactions
   - View financial summaries
   - Generate visualizations
   - Access predictive analytics

## Data Structure

The system uses a CSV file (`data.csv`) with the following columns:
- Date (DD-MM-YYYY format)
- Amount
- Currency
- Use (Transaction category)
- Comment

## Project Structure

```
├── main.py              # Main program file
├── core.py             # Core CSV operations
├── functions.py        # Utility functions
├── Filter_data.py      # Data filtering operations
├── graphing.py         # Visualization functions
├── predictions.py      # Financial predictions
├── logs.py            # Logging functionality
├── users.py           # User management
├── data.csv           # Transaction data
├── requirements.txt   # Project dependencies
└── README.md          # This file
```

## Features in Detail

### Transaction Management
- Add transactions with date, amount, currency, use case, and comments
- View all transactions in a formatted table
- Edit existing transactions
- Delete unwanted transactions

### Data Analysis
- Filter transactions by various criteria
- Generate monthly summaries
- View overall financial summaries
- Analyze spending patterns

### Visualizations
- Interactive charts and graphs
- Trend analysis
- Distribution analysis
- Comparative analysis

### Predictive Features
- Future financial predictions
- Trend analysis
- Accuracy metrics
- Comparison with historical data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python
- Uses various data science and visualization libraries
- Implements machine learning for predictions
- Machine Learning and this readme.md is written with the help of AI.