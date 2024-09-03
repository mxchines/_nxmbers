# config.py
db_host = "numbermxchine.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
db_name = "nxmbers"
db_user = "mxchinist"
db_password = "foJzyn-miwhor-bavpo4"
db_port = 5432

forecast_horizon = 12
# ... other variables

# config.py
ALPHA_VANTAGE_API_KEY = "KXUK213E0W7JLEQV"
BEAM_API_KEY = "NmJkNzkxNGQtYzUwMy00YjAzLTkyMzYtODUxMmJlYWJmY2M1"

DEFAULT_TICKER = 'AAPL'
DEFAULT_START_DATE = '2000-01-01'
DEFAULT_END_DATE = '2024-08-01'
DEFAULT_INTERVAL = '1day'
DEFAULT_API_SOURCES = ['beam', 'alpha']

# User input values (to be updated by the frontend)
USER_TICKER = DEFAULT_TICKER
USER_START_DATE = DEFAULT_START_DATE
USER_END_DATE = DEFAULT_END_DATE
USER_INTERVAL = DEFAULT_INTERVAL
USER_API_SOURCES = DEFAULT_API_SOURCES
