from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import config
from data_ingestion.data_fetcher import main as fetch_data

app = Flask(__name__)

@app.route('/api/update-config', methods=['POST'])
def update_config():
    data = request.json
    config.USER_TICKER = data.get('ticker', config.DEFAULT_TICKER)
    config.USER_START_DATE = data.get('startDate', config.DEFAULT_START_DATE)
    config.USER_END_DATE = data.get('endDate', config.DEFAULT_END_DATE)
    config.USER_INTERVAL = data.get('interval', config.DEFAULT_INTERVAL)
    config.USER_API_SOURCE = data.get('apiSource', 'yahoo')  # Default to Yahoo if not specified

    # Execute data_fetcher.py with the updated configuration
    try:
        fetch_data(
            ticker=config.USER_TICKER,
            start_date=config.USER_START_DATE,
            end_date=config.USER_END_DATE,
            interval=config.USER_INTERVAL
        )
        return jsonify({"message": "Configuration updated and data fetched successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html', 
                           default_ticker=config.DEFAULT_TICKER,
                           default_start_date=config.DEFAULT_START_DATE,
                           default_end_date=config.DEFAULT_END_DATE,
                           default_interval=config.DEFAULT_INTERVAL,
                           default_api_source=config.DEFAULT_API_SOURCE)

if __name__ == '__main__':
    app.run(debug=True)