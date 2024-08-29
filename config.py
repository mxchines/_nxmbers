# config.py
db_host = "numbermxchine.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
db_name = "nxmbers"
db_user = "mxchinist"
db_password = "foJzyn-miwhor-bavpo4"
db_port = 5432

forecast_horizon = 12
# ... other variables

# Configuration settings for the stock data fetcher

# Default values
DEFAULT_TICKER = 'AAPL'
DEFAULT_START_DATE = '2020-01-01'
DEFAULT_END_DATE = '2023-01-01'
DEFAULT_INTERVAL = '1d'
DEFAULT_API_KEY = '05CH528CFTOVYQ1B'

# User input values (to be updated by the frontend)
USER_TICKER = DEFAULT_TICKER
USER_START_DATE = DEFAULT_START_DATE
USER_END_DATE = DEFAULT_END_DATE
USER_INTERVAL = DEFAULT_INTERVAL
USER_API_KEY = DEFAULT_API_KEY