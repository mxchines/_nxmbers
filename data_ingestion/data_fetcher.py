import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

def fetch_yahoo_finance_data(ticker, start_date, end_date, interval='1d'):
    """
    Fetch historical market data from Yahoo Finance.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        start_date: Start date for fetching data (e.g., '2020-01-01')
        end_date: End date for fetching data (e.g., '2023-01-01')
        interval: Data interval ('1d' for daily, '1h' for hourly)

    Returns:
        DataFrame containing OHLCV data
    """
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data

def fetch_alpha_vantage_data(ticker, interval='daily', api_key='05CH528CFTOVYQ1B'):
    """
    Fetch historical market data from Alpha Vantage.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        interval: Data interval ('daily', '60min', '5min')
        api_key: Alpha Vantage API key

    Returns:
        DataFrame containing OHLCV data
    """
    ts = TimeSeries(key=api_key, output_format='pandas')

    if interval == 'daily':
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    elif interval == '60min':
        data, meta_data = ts.get_intraday(symbol=ticker, interval='60min', outputsize='full')
    else:
        raise ValueError("Unsupported interval for Alpha Vantage: {}".format(interval))

    # Rename columns to standard OHLCV
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return data

def combine_data(yahoo_data, alpha_data):
    """
    Combine Yahoo Finance and Alpha Vantage data.

    Args:
        yahoo_data: DataFrame from Yahoo Finance
        alpha_data: DataFrame from Alpha Vantage

    Returns:
        Combined DataFrame with a date column
    """
    # Reset index to make date a column for both dataframes
    yahoo_data = yahoo_data.reset_index()
    alpha_data = alpha_data.reset_index()

    # Rename date column to ensure consistency
    yahoo_data = yahoo_data.rename(columns={'Date': 'date'})
    alpha_data = alpha_data.rename(columns={'date': 'date'})

    # Combine the data
    combined_data = pd.merge(yahoo_data, alpha_data, on='date', how='outer', suffixes=('_yahoo', '_alpha'))

    # Sort the combined data by date
    combined_data = combined_data.sort_values('date')

    return combined_data

def main():
    # Fetch Yahoo Finance data
    ticker = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2023-01-01'
    interval = '1d'

    yahoo_data = fetch_yahoo_finance_data(ticker, start_date, end_date, interval)

    # Fetch Alpha Vantage data
    api_key = '05CH528CFTOVYQ1B'  # Your Alpha Vantage API key
    alpha_data = fetch_alpha_vantage_data(ticker, 'daily', api_key)

    # Combine the data
    combined_data = combine_data(yahoo_data, alpha_data)

    # Save the combined data to a CSV file
    combined_data.to_csv('../data_storage/csv/combined_data.csv', index=False)
    print("Data aggregation complete. Combined data saved to 'combined_data.csv'.")

if __name__ == "__main__":
    main()