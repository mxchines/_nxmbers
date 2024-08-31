import pandas as pd
from path_utility import get_data_path

def combine_data(yahoo_data, alpha_data):
    """
    Combine Yahoo Finance and Alpha Vantage data.
    """
    # Reset index for all dataframes
    yahoo_data = yahoo_data.reset_index()
    alpha_data = alpha_data.reset_index()

    # Ensure consistent date column naming
    yahoo_data = yahoo_data.rename(columns={'Date': 'date'})
    alpha_data = alpha_data.rename(columns={'date': 'date'})

    # Merge dataframes
    combined_data = pd.merge(yahoo_data, alpha_data, on='date', how='outer', suffixes=('_yahoo', '_alpha'))

    # Sort by date
    combined_data = combined_data.sort_values('date')

    return combined_data

def main(ticker):
    yahoo_csv_path = get_data_path(__file__, f'{ticker}_yahoo_data.csv')
    alpha_csv_path = get_data_path(__file__, f'{ticker}_alpha_data.csv')

    yahoo_data = pd.read_csv(yahoo_csv_path, parse_dates=['date'])
    alpha_data = pd.read_csv(alpha_csv_path, parse_dates=['date'])

    combined_data = combine_data(yahoo_data, alpha_data)

    combined_csv_path = get_data_path(__file__, f'{ticker}_combined_data.csv')
    combined_data.to_csv(combined_csv_path, index=False)

    print(f"Data combination complete for {ticker}.")
    print(f"Combined data saved to '{combined_csv_path}'")

if __name__ == "__main__":
    # This default value will be overridden when called from the main application
    main('AAPL')