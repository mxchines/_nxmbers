from flask import Flask, request, jsonify, render_template
import config
from config import USER_TICKER, USER_START_DATE, USER_END_DATE, USER_INTERVAL, USER_API_SOURCES, BEAM_API_KEY
import logging
import sys
import os

# Get the current directory
current_dir = os.path.dirname(__file__)

# Add the necessary paths to sys.path
sys.path.insert(0, os.path.join(current_dir, '../data_cleaning'))
sys.path.insert(0, os.path.join(current_dir, '../data_storage'))
sys.path.insert(0, os.path.join(current_dir, '../data_ingestion'))

# Print out the sys.path variable
print(sys.path)

# Import the necessary modules
from data_ingestion.data_fetcher import main as fetch_data
from data_cleaning.data_cleaner import clean_data  # Corrected import
from data_storage.rds_uploader import main as rds_uploader_main

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_config_data(ticker, start_date, end_date, interval, api_sources, beam_api_key):
    # Fetch data
    fetch_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        api_sources=api_sources,
        beam_api_key=beam_api_key
    )

    # Clean data
    clean_data()

@app.route('/api/update-config', methods=['POST'])
def update_config():
    data = request.json
    ticker = data.get('ticker', USER_TICKER)
    start_date = data.get('startDate', USER_START_DATE)
    end_date = data.get('endDate', USER_END_DATE)
    interval = data.get('interval', USER_INTERVAL)
    api_sources = data.get('apiSources', USER_API_SOURCES)

    update_config_data(ticker, start_date, end_date, interval, api_sources, BEAM_API_KEY)

    return jsonify({"message": "Data updated successfully"}), 200

@app.route('/')
def index():
    return render_template('index.html', 
                           default_ticker=config.DEFAULT_TICKER,
                           default_start_date=config.DEFAULT_START_DATE,
                           default_end_date=config.DEFAULT_END_DATE,
                           default_interval=config.DEFAULT_INTERVAL,
                           default_api_sources=config.DEFAULT_API_SOURCES)

if __name__ == '__main__':
    app.run(debug=True)