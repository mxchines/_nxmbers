import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import pandas as pd
import logging
import os
import socket

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load R libraries
base = importr('base')
DBI = importr('DBI')
RPostgres = importr('RPostgres')
forecast = importr('forecast')
stats = importr('stats')

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

    # Log data info
    logging.info(f"Data info:\n{pdf.info()}")
    logging.info(f"Data description:\n{pdf.describe()}")
    logging.info(f"Data head:\n{pdf.head()}")

    # Convert back to R dataframe
    with localconverter(ro.default_converter + pandas2ri.converter):
        data = ro.conversion.py2rpy(pdf)

    # Convert data to time series
    ts_data = stats.ts(data.rx2('close_alpha'), frequency=365, start=ro.FloatVector([pdf['date'].dt.year.min(), pdf['date'].dt.dayofyear.min()]))

    # Fit ARIMA model
    logging.info("Fitting ARIMA model...")
    arima_model = forecast.auto_arima(ts_data, stepwise=True, approximation=False)

    # Print model summary
    logging.info("ARIMA Model Summary:")
    print(base.summary(arima_model))

    # Generate forecasts
    logging.info("Generating forecasts...")
    forecasts = forecast.forecast_ar(arima_model, h=15)  # Generate 15 days of forecast directly

    # Extract forecast data
    forecast_mean = ro.r('as.numeric')(forecasts.rx2('mean'))
    forecast_lower = ro.r('as.numeric')(forecasts.rx2('lower')[0])
    forecast_upper = ro.r('as.numeric')(forecasts.rx2('upper')[0])

    # Plot the forecasts
    logging.info("Plotting forecasts...")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.plot(pdf['date'], pdf['close_alpha'], label='Actual')
    forecast_dates = pd.date_range(start=pdf['date'].iloc[-1] + pd.Timedelta(days=1), periods=15, freq='D')
    plt.plot(forecast_dates, forecast_mean, label='Forecast', color='red')
    plt.fill_between(forecast_dates, forecast_lower, forecast_upper, color='red', alpha=0.2)
    plt.title('ARIMA Forecast')
    plt.xlabel('Date')
    plt.ylabel('Close Alpha')
    plt.legend()

    # Ensure directory exists before saving
    os.makedirs('../nxmbers/data/plots/png', exist_ok=True)
    plt.savefig('../nxmbers/data/plots/png/forecast_plot.png')

    logging.info("Analysis complete! Plot saved as forecast_plot.png")

except socket.gaierror as e:
    logging.error(f"Failed to resolve hostname: {str(e)}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")
except ValueError as ve:
    logging.error(f"Value error occurred: {str(ve)}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")

finally:
    # Ensure database connection is closed if it was opened
    if 'con' in locals() and con is not None:
        DBI.dbDisconnect(con)