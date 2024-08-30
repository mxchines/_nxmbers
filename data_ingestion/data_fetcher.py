import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import requests
import pandas as pd
from path_utility import get_data_path
from data_cleaning.data_cleaner import clean_data  # Import the clean_data function

ALPHA_VANTAGE_API_KEY = "KXUK213E0W7JLEQV"
TWELVE_DATA_API_KEY = "2409a8dd5abd488e8d833f929476b034"

def fetch_yahoo_finance_data(ticker, start_date, end_date, interval='1d'):
    """
    Fetch historical market data from Yahoo Finance.
    """
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data

def fetch_alpha_vantage_data(ticker, interval='daily'):
    """
    Fetch historical market data from Alpha Vantage.
    """
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')

    if interval == 'daily':
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    elif interval == '60min':
        data, meta_data = ts.get_intraday(symbol=ticker, interval='60min', outputsize='full')
    else:
        raise ValueError(f"Unsupported interval for Alpha Vantage: {interval}")

    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return data

def fetch_twelve_data(ticker, start_date, end_date, interval='1day'):
    """
    Fetch historical market data from Twelve Data.
    """
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": ticker,
        "interval": interval,
        "start_date": start_date,
        "end_date": end_date,
        "apikey": TWELVE_DATA_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'values' not in data:
        raise ValueError(f"Error fetching data from Twelve Data: {data.get('message', 'Unknown error')}")
    
    df = pd.DataFrame(data['values'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.sort_index()
    return df

import os

def main(ticker, start_date, end_date, interval='1d'):
    # Fetch data from all three sources
    yahoo_data = fetch_yahoo_finance_data(ticker, start_date, end_date, interval)
    alpha_data = fetch_alpha_vantage_data(ticker, 'daily')
    twelve_data = fetch_twelve_data(ticker, start_date, end_date)

    # Create 'csv' subdirectory if it doesn't exist
    csv_dir = get_data_path(__file__, 'csv')
    os.makedirs(csv_dir, exist_ok=True)

    # Save individual datasets
    yahoo_csv_path = os.path.join(csv_dir, f'{ticker}_yahoo_data.csv')
    alpha_csv_path = os.path.join(csv_dir, f'{ticker}_alpha_data.csv')
    twelve_csv_path = os.path.join(csv_dir, f'{ticker}_twelve_data.csv')

    yahoo_data.to_csv(yahoo_csv_path)
    alpha_data.to_csv(alpha_csv_path)
    twelve_data.to_csv(twelve_csv_path)

    print(f"Data fetching complete for {ticker}.")
    print(f"Yahoo Finance data saved to '{yahoo_csv_path}'")
    print(f"Alpha Vantage data saved to '{alpha_csv_path}'")
    print(f"Twelve Data data saved to '{twelve_csv_path}'")

if __name__ == "__main__":
    # These default values will be overridden when called from the main application
    main('AAPL', '2020-01-01', '2023-01-01')

    print(f"Data fetching complete for {ticker}.")
    print(f"Yahoo Finance data saved to '{yahoo_csv_path}'")
    print(f"Alpha Vantage data saved to '{alpha_csv_path}'")
    print(f"Twelve Data data saved to '{twelve_csv_path}'")

     # Trigger data cleaning process
    try:
        clean_data()
        print("Data cleaning process completed successfully.")
    except Exception as e:
        print(f"Error during data cleaning: {str(e)}")

    return "Data fetching and cleaning completed successfully."

if __name__ == "__main__":
    # These default values will be overridden when called from the main application
    main('AAPL', '2020-01-01', '2023-01-01')