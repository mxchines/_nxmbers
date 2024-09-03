import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import pandas as pd
import numpy as np
import logging
import os
import socket
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load R libraries
base = importr('base')
DBI = importr('DBI')
RPostgres = importr('RPostgres')

# Database connection parameters
db_host = "numbermxchine.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
db_name = "nxmbers"
db_user = "mxchinist"
db_password = "foJzyn-miwhor-bavpo4"
db_port = 5432

try:
    # Resolve hostname to IP address
    logging.info(f"Resolving hostname: {db_host}")
    db_ip = socket.gethostbyname(db_host)
    logging.info(f"Resolved IP: {db_ip}")

    # Connect to the database
    logging.info("Connecting to the database...")
    con = DBI.dbConnect(RPostgres.Postgres(),
                        host=db_ip,
                        dbname=db_name,
                        user=db_user,
                        password=db_password,
                        port=db_port)

    # Fetch data from the database 
    logging.info("Fetching data from the database...")
    query = "SELECT date, close_alpha FROM market_data_2024_08_28_090019 ORDER BY date"
    data = DBI.dbGetQuery(con, query)

    # Close the database connection
    DBI.dbDisconnect(con)

    # Check if data is empty
    if data.nrow == 0:
        raise ValueError("No data returned from the database query")

    # Convert R dataframe to pandas dataframe
    logging.info("Converting data to pandas dataframe...")
    with localconverter(ro.default_converter + pandas2ri.converter):
        pdf = ro.conversion.rpy2py(data)

    # Convert 'date' column to datetime without timezone
    pdf['date'] = pd.to_datetime(pdf['date'], errors='coerce').dt.tz_localize(None)

    # Ensure 'close_alpha' is numeric
    pdf['close_alpha'] = pd.to_numeric(pdf['close_alpha'], errors='coerce')

    # Remove NaN values
    pdf = pdf.dropna()

    # Set date as index
    pdf.set_index('date', inplace=True)

    # Log data info
    logging.info(f"Data info:\n{pdf.info()}")
    logging.info(f"Data description:\n{pdf.describe()}")
    logging.info(f"Data head:\n{pdf.head()}")

    # Automatically select ARIMA parameters
    logging.info("Selecting ARIMA parameters...")
    auto_model = auto_arima(pdf['close_alpha'], seasonal=False, stepwise=True, suppress_warnings=True, error_action="ignore", max_order=None)
    
    # Get the order from auto_arima
    order = auto_model.order

    # Fit ARIMA model
    logging.info("Fitting ARIMA model...")
    model = ARIMA(pdf['close_alpha'], order=order)
    results = model.fit()

    # Generate forecasts
    logging.info("Generating forecasts...")
    forecast = results.forecast(steps=15)
    forecast_index = pd.date_range(start=pdf.index[-1] + pd.Timedelta(days=1), periods=15)
    forecast = pd.Series(forecast, index=forecast_index)

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pdf.index, y=pdf['close_alpha'], name='Actual'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast, name='Forecast'))

    # Add zooming and interactive controls
    fig.update_layout(title='ARIMA Forecast', xaxis_title='Date', yaxis_title='Close')
    fig.update_layout(dragmode='pan', 
                      xaxis=dict(type='date', autorange=True, fixedrange=False),
                      yaxis=dict(autorange=True, fixedrange=False))
    fig.update_xaxes(rangeslider_visible=True, 
                     rangeselector=dict(
                         buttons=[
                             dict(count=1, label='1m', step='month', stepmode='backward'),
                             dict(count=6, label='6m', step='month', stepmode='backward'),
                             dict(count=1, label='1y', step='year', stepmode='backward'),
                             dict(step='all')
                         ]
                     ))

    # Show the plot
    fig.show()

    # Plot the forecasts using matplotlib
    logging.info("Plotting forecasts...")
    plt.figure(figsize=(12, 6))
    plt.plot(pdf.index, pdf['close_alpha'], label='Actual')
    plt.plot(forecast.index, forecast, label='Forecast', color='red')
    plt.title('ARIMA Forecast')
    plt.xlabel('Date')
    plt.ylabel('Close Alpha')
    plt.legend()

    # Ensure directory exists before saving
    os.makedirs('../nxmbers/nxmbers/data/plots/png', exist_ok=True)
    plt.savefig('../nxmbers/nxmbers/data/plots/png/arima_forecast_plot.png')

    logging.info("Analysis complete! Plot saved as arima_forecast_plot.png")

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
finally:
    # Ensure the database connection is closed
    if 'con' in locals() and con is not None:
        DBI.dbDisconnect(con)
    logging.info("Script execution completed.")