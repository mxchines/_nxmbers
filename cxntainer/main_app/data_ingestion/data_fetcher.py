import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from path_utility import get_data_path
import config
import logging
import requests

import sys
import os

# Get the current directory of data_fetcher.py
current_dir = os.path.dirname(__file__)

# Add the path to the data_cleaning directory
sys.path.insert(0, os.path.join(current_dir, '../data_cleaning'))

# Now you can import data_cleaner
from data_cleaner import clean_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_beam_data(ticker, start_date, end_date, interval, api_key):
    beam_url = 'https://api.beamapi.com/data/fundamentals/us/sec/form_4/v1'
    transport = RequestsHTTPTransport(
        url=beam_url,
        headers={'Authorization': f'Bearer {api_key}'},
        use_json=True,
    )

    try:
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql('''
        query FetchStockData($ticker: String!, $startDate: Date!, $endDate: Date!, $interval: Interval!) {
            stockData(ticker: $ticker, startDate: $startDate, endDate: $endDate, interval: $interval) {
                date
                open
                high
                low
                close
                volume
                adjustedClose
            }
        }
        ''')

        variables = {
            'ticker': ticker,
            'startDate': start_date,
            'endDate': end_date,
            'interval': interval,
        }

        result = client.execute(query, variable_values=variables)
        
        df = pd.DataFrame(result['stockData'])
        df['date'] = pd.to_datetime(df['date'])
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
        df['source'] = 'beam'
        return df
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
    except Exception as e:
        logger.error(f"Failed to fetch data from Beam API: {str(e)}")
    return None

def fetch_alpha_vantage_data(ticker, start_date, end_date, interval):
    try:
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
    except Exception as e:
        logger.error(f"Failed to fetch data from Alpha Vantage API: {str(e)}")
        return None

def save_data(data, ticker, source):
    if data is not None and not data.empty:
        output_dir = get_data_path(__file__, 'csv')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{ticker}_{source}_data.csv')
        data.to_csv(output_file, index=False)
        logger.info(f"{source.capitalize()} data saved to {output_file}")
    else:
        logger.warning(f"No data to save for {ticker} from {source}")

def main(ticker, start_date, end_date, interval, api_sources, beam_api_key):
    data_fetched = False
    for source in api_sources:
        if source == 'beam':
            beam_data = fetch_beam_data(ticker, start_date, end_date, interval, beam_api_key)
            if beam_data is not None:
                save_data(beam_data, ticker, 'beam')
                data_fetched = True
            else:
                logger.warning("Falling back to Alpha Vantage due to Beam API failure")
                api_sources = ['alpha']  # Fall back to Alpha Vantage
        elif source == 'alpha':
            alpha_data = fetch_alpha_vantage_data(ticker, start_date, end_date, interval)
            if alpha_data is not None:
                save_data(alpha_data, ticker, 'alpha_vantage')
                data_fetched = True

    if data_fetched:
        import os
        import sys
        sys.path.insert(0, '../data_cleaning')
        from data_cleaner import clean_data
        clean_data()
        return f"Data fetching completed successfully for {ticker} from available sources"
    else:
        return f"Failed to fetch data for {ticker} from any source"

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    interval = "1d"
    api_sources = ['beam', 'alpha']
    beam_api_key = config.BEAM_API_KEY
    result = main(ticker, start_date, end_date, interval, api_sources, beam_api_key)
    print(result)