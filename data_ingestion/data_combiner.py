import pandas as pd
from path_utility import get_data_path

def combine_data(yahoo_data, alpha_data, twelve_data):
    """
    Combine Yahoo Finance, Alpha Vantage, and Twelve Data data.
    """
    # Reset index for all dataframes
    yahoo_data = yahoo_data.reset_index()
    alpha_data = alpha_data.reset_index()
    twelve_data = twelve_data.reset_index()

    # Ensure consistent date column naming
    yahoo_data = yahoo_data.rename(columns={'Date': 'date'})
    alpha_data = alpha_data.rename(columns={'date': 'date'})
    twelve_data = twelve_data.rename(columns={'datetime': 'date'})

    # Merge all dataframes
    combined_data = pd.merge(yahoo_data, alpha_data, on='date', how='outer', suffixes=('_yahoo', '_alpha'))
    combined_data = pd.merge(combined_data, twelve_data, on='date', how='outer', suffixes=('', '_twelve'))

    # Sort by date
    combined_data = combined_data.sort_values('date')

    return combined_data

def main(ticker):
    yahoo_csv_path = get_data_path(__file__, f'{ticker}_yahoo_data.csv')
    alpha_csv_path = get_data_path(__file__, f'{ticker}_alpha_data.csv')
    twelve_csv_path = get_data_path(__file__, f'{ticker}_twelve_data.csv')

    yahoo_data = pd.read_csv(yahoo_csv_path, index_col=0, parse_dates=True)
    alpha_data = pd.read_csv(alpha_csv_path, index_col=0, parse_dates=True)
    twelve_data = pd.read_csv(twelve_csv_path, index_col=0, parse_dates=True)

    combined_data = combine_data(yahoo_data, alpha_data, twelve_data)

    combined_csv_path = get_data_path(__file__, f'{ticker}_combined_data.csv')
    combined_data.to_csv(combined_csv_path, index=False)

    print(f"Data combination complete for {ticker}.")
    print(f"Combined data saved to '{combined_csv_path}'")

if __name__ == "__main__":
    # This default value will be overridden when called from the main application
    main('AAPL')