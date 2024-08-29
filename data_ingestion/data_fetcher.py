import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from path_utility import get_data_path

def fetch_yahoo_finance_data(ticker, start_date, end_date, interval='1d'):
    """
    Fetch historical market data from Yahoo Finance.
    """
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data

def fetch_alpha_vantage_data(ticker, interval='daily', api_key='05CH528CFTOVYQ1B'):
    """
    Fetch historical market data from Alpha Vantage.
    """
    ts = TimeSeries(key=api_key, output_format='pandas')

    if interval == 'daily':
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    elif interval == '60min':
        data, meta_data = ts.get_intraday(symbol=ticker, interval='60min', outputsize='full')
    else:
        raise ValueError(f"Unsupported interval for Alpha Vantage: {interval}")

    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return data

def combine_data(yahoo_data, alpha_data):
    """
    Combine Yahoo Finance and Alpha Vantage data.
    """
    yahoo_data = yahoo_data.reset_index()
    alpha_data = alpha_data.reset_index()

    yahoo_data = yahoo_data.rename(columns={'Date': 'date'})
    alpha_data = alpha_data.rename(columns={'date': 'date'})

    combined_data = pd.merge(yahoo_data, alpha_data, on='date', how='outer', suffixes=('_yahoo', '_alpha'))
    combined_data = combined_data.sort_values('date')

    return combined_data

def main(ticker, start_date, end_date, interval='1d', api_key='05CH528CFTOVYQ1B'):
    yahoo_data = fetch_yahoo_finance_data(ticker, start_date, end_date, interval)
    alpha_data = fetch_alpha_vantage_data(ticker, 'daily', api_key)

    combined_data = combine_data(yahoo_data, alpha_data)

    csv_path = get_data_path(__file__, 'combined_data.csv')
    combined_data.to_csv(csv_path, index=False)
    print(f"Data aggregation complete for {ticker}. Combined data saved to 'combined_data.csv'.")

if __name__ == "__main__":
    # These default values will be overridden when called from the main application
    main('AAPL', '2020-01-01', '2023-01-01')