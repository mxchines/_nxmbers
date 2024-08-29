import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
import pandas as pd

# Assuming 'data' is your R dataframe
# Convert R dataframe to pandas dataframe
pandas2ri.activate()
pdf = pandas2ri.rpy2py(data)

# Convert 'date' column to datetime
pdf['date'] = pd.to_datetime(pdf['date'])

# Convert back to R dataframe
data = pandas2ri.py2rpy(pdf)

# Now proceed with the rest of your script
ts_data = ro.r.ts(data.rx2('close_alpha'), frequency=12)

# Rest of your ARIMA modeling code...
import rpy2.robjects as ro
from rpy2.robjects.packages import importr

# Load R libraries
base = importr('base')
DBI = importr('DBI')
RPostgres = importr('RPostgres')
forecast = importr('forecast')
grdevices = importr('grDevices')
ggplot2 = importr('ggplot2')

# For progress bar
from tqdm import tqdm

# For plotting
import matplotlib.pyplot as plt
from rpy2.robjects.lib import ggplot2
from rpy2.robjects import pandas2ri

# Database connection parameters
db_host = "numbermxchine.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
db_name = "nxmbers"
db_user = "mxchinist"
db_password = "foJzyn-miwhor-bavpo4"
db_port = 5432

# Connect to the database
con = DBI.dbConnect(RPostgres.Postgres(),
                    host=db_host,
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    port=db_port)

# Fetch data from the database 
query = "SELECT date, close_alpha FROM market_data_2024_08_28_090019 ORDER BY date"
data = DBI.dbGetQuery(con, query)

# Close the database connection
DBI.dbDisconnect(con)

# Inspect the data
print(data)

# Check if data is empty
if data.nrow == 0:
    raise ValueError("No data returned from the database query.")

# Convert 'date' column to R Date format (corrected assignment)
data.rx2['date'] = ro.r('`[[<-`')(data, 'date', value = ro.r('as.Date')(data.rx2['date'], origin = '1970-01-01')) 

# Handle missing values and convert 'close_alpha' to numeric
data = ro.r('na.omit')(data)
data.rx2['close_alpha'] = ro.r('as.numeric')(data.rx2['close_alpha'])

# Convert data to time series (adjust frequency if not monthly)
ts_data = ro.r.ts(data.rx2('close_alpha'), frequency=12)

# Handle missing values and convert to numeric 
data = ro.r('na.omit')(data)
data.rx2['close_alpha'] = ro.r('`[[<-`')(data, 'close_alpha', value=ro.r('as.numeric')(data.rx2['close_alpha'])) 

# Convert data to time series (adjust frequency if not monthly)
ts_data = ro.r.ts(data.rx2('close_alpha'), frequency=12) 

# Create a tqdm progress bar
pb = tqdm(total=100)

# Function to update progress bar
def update_progress(value):
    pb.update(int(value / 100 * pb.total))

# Fit ARIMA model with progress updates
arima_model = forecast.auto_arima(ts_data, stepwise=False, approximation=False,
                                 parallel=True, num_cores=2,
                                 callback=update_progress)

# Print model summary
print(base.summary(arima_model))

# Generate forecasts
forecasts = forecast.forecast(arima_model, h=12)

# Close the progress bar
pb.close()

# Plot the forecasts using matplotlib
grdevices.png(file="forecast_plot.png", width=800, height=600)
p = ggplot2.autoplot(forecasts)
p.plot()
grdevices.dev_off()

print("Analysis complete! Plot saved as forecast_plot.png")