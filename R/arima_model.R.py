import psycopg2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd
from tqdm import tqdm
import time

# Activate automatic conversion
pandas2ri.activate() 

# Import R packages
forecast = importr('forecast')

print("Starting ARIMA model script...")

# Database connection details
dbname = "nxmbers"
user = "mxchinist"
password = "foJzyn-miwhor-bavpo4"
host = "nxmbers.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
port = 5432

print("Connecting to the database...")
# Connect to the PostgreSQL database
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create a cursor object
cur = conn.cursor()

print("Executing query to fetch data...")
# Execute a query to fetch data
query = "SELECT date, close_alpha FROM market_data_2024_08_28_090019"
cur.execute(query)

print("Fetching all rows from the result...")
# Fetch all the rows from the result
data = cur.fetchall()

# Close the cursor and the connection
cur.close()
conn.close()
print("Database connection closed.")

print("Converting fetched data into a Pandas DataFrame...")
# Convert the fetched data into a Pandas DataFrame
df = pd.DataFrame(data, columns=['date', 'close_alpha'])

# Convert date column to datetime if needed
df['date'] = pd.to_datetime(df['date'])

print("Converting Pandas DataFrame to R DataFrame...")
# Convert Pandas DataFrame to R DataFrame
r_df = pandas2ri.py2rpy(df)

print("Creating time series in R...")
# Create time series in R
r_ts_data = robjects.r('ts')(r_df['close_alpha'], frequency=12) 

print("Fitting ARIMA model...")
# Fit ARIMA model
r_model = forecast.auto_arima(r_ts_data)

print("Generating predictions...")
# Generate predictions
r_predictions = forecast.forecast(r_model, h=12)

print("Converting predictions back to Python...")
# Convert predictions back to Python
predictions = pandas2ri.rpy2py(r_predictions)

print("Processing predictions...")
# Simulating some processing time with a loading bar
for _ in tqdm(range(10), desc="Processing predictions"):
    time.sleep(0.5)  # Simulating some work being done

print("\nPredictions:")
print(predictions)

print("Script execution completed.")