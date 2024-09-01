from flask import Flask, request, jsonify, render_template
import config
from data_ingestion.data_fetcher import main as fetch_data
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/update-config', methods=['POST'])
def update_config():
    data = request.json
    config.USER_TICKER = data.get('ticker', config.DEFAULT_TICKER)
    config.USER_START_DATE = data.get('startDate', config.DEFAULT_START_DATE)
    config.USER_END_DATE = data.get('endDate', config.DEFAULT_END_DATE)
    config.USER_INTERVAL = data.get('interval', config.DEFAULT_INTERVAL)
    config.USER_API_SOURCES = data.get('apiSources', config.DEFAULT_API_SOURCES)

    try:
        result = fetch_data(
            ticker=config.USER_TICKER,
            start_date=config.USER_START_DATE,
            end_date=config.USER_END_DATE,
            interval=config.USER_INTERVAL,
            api_sources=config.USER_API_SOURCES,
            beam_api_key=config.BEAM_API_KEY
        )
        return jsonify({"message": result}), 200
    except Exception as e:
        logger.error(f"Error in update_config: {str(e)}")
        return jsonify({"error": "An error occurred while fetching data. Please try again."}), 500

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