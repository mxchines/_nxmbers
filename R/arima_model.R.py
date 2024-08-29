import psycopg2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# Activate automatic conversion
pandas2ri.activate() 

# Import R packages
forecast = importr('forecast')

# Database connection details
dbname = "nxmbers"
user = "mxchinist"
password = "foJzyn-miwhor-bavpo4"
host = "nxmbers.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
port = 5432

# Connect to the PostgreSQL database
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create a cursor object
cur = conn.cursor()

# Execute a query to fetch data
query = "SELECT date, close_alpha FROM market_data_2024_08_28_090019"
cur.execute(query)

# Fetch all the rows from the result
data = cur.fetchall()

# Close the cursor and the connection
cur.close()
conn.close()

# Convert the fetched data into a Pandas DataFrame
import pandas as pd
df = pd.DataFrame(data, columns=['date', 'close_alpha'])

# Convert date column to datetime if needed
df['date'] = pd.to_datetime(df['date'])

# Convert Pandas DataFrame to R DataFrame
r_df = pandas2ri.py2rpy(df)

# Create time series in R
r_ts_data = robjects.r('ts')(r_df['close_alpha'], frequency=12) 

# Fit ARIMA model
r_model = forecast.auto_arima(r_ts_data)

# Generate predictions
r_predictions = forecast.forecast(r_model, h=12)

# Convert predictions back to Python
predictions = pandas2ri.rpy2py(r_predictions)

# Print or further process the predictions in Python
print(predictions)