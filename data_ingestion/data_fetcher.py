import yfinance as yf
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from twelvedata import TDClient
import os
from path_utility import get_data_path
import config

def fetch_yahoo_data(ticker, start_date, end_date, interval):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data.reset_index(inplace=True)
    data.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    data['source'] = 'yahoo'
    return data

def fetch_alpha_vantage_data(ticker, start_date, end_date, interval):
    ts = TimeSeries(key=config.ALPHA_VANTAGE_API_KEY)
    data, _ = ts.get_daily(symbol=ticker, outputsize='full')
    df = pd.DataFrame(data).T
    df.index = pd.to_datetime(df.index)
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    df.reset_index(inplace=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['adj_close'] = df['close']
    df['source'] = 'alpha_vantage'
    return df

def fetch_twelve_data(ticker, start_date, end_date, interval):
    td = TDClient(apikey=config.TWELVE_DATA_API_KEY)
    data = td.time_series(
        symbol=ticker,
        interval=interval,
        start_date=start_date,
        end_date=end_date
    ).as_pandas()
    data.reset_index(inplace=True)
    data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    data['adj_close'] = data['close']
    data['source'] = 'twelve_data'
    return data

def fetch_and_combine_data(ticker, start_date, end_date, interval):
    yahoo_data = fetch_yahoo_data(ticker, start_date, end_date, interval)
    alpha_data = fetch_alpha_vantage_data(ticker, start_date, end_date, interval)
    twelve_data = fetch_twelve_data(ticker, start_date, end_date, interval)
    
    combined_data = pd.concat([yahoo_data, alpha_data, twelve_data], ignore_index=True)
    combined_data.sort_values('date', inplace=True)
    return combined_data

def save_data(data, ticker):
    output_dir = get_data_path(__file__, 'csv')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{ticker}_data.csv')
    data.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")

def main(ticker, start_date, end_date, interval):
    combined_data = fetch_and_combine_data(ticker, start_date, end_date, interval)
    save_data(combined_data, ticker)
    return f"Data fetching and combining completed successfully for {ticker}"

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    interval = "1d"
    main(ticker, start_date, end_date, interval)