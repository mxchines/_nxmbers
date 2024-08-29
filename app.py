from flask import Flask, request, jsonify
import config

app = Flask(__name__)

@app.route('/api/update-config', methods=['POST'])
def update_config():
    data = request.json
    config.USER_TICKER = data.get('ticker', config.DEFAULT_TICKER)
    config.USER_START_DATE = data.get('startDate', config.DEFAULT_START_DATE)
    config.USER_END_DATE = data.get('endDate', config.DEFAULT_END_DATE)
    config.USER_INTERVAL = data.get('interval', config.DEFAULT_INTERVAL)
    config.USER_API_KEY = data.get('apiKey', config.DEFAULT_API_KEY)
    
    return jsonify({"message": "Configuration updated successfully"}), 200

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)