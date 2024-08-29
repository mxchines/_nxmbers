# Load required libraries
library(DBI)
library(RMySQL)  # Assuming MySQL database, adjust if using a different database
library(forecast)

# Database connection parameters
db_host <- "your_host"
db_name <- "your_database"
db_user <- "your_username"
db_password <- "your_password"

# Connect to the database
con <- dbConnect(MySQL(), host = db_host, dbname = db_name, user = db_user, password = db_password)

# Fetch data from the database
query <- "SELECT date, value FROM your_table ORDER BY date"
data <- dbGetQuery(con, query)

# Close the database connection
dbDisconnect(con)

# Convert the data to a time series object
# Assuming 'date' is in a format that can be converted to Date
data$date <- as.Date(data$date)
ts_data <- ts(data$value, frequency = 12)  # Adjust frequency if needed

# Fit ARIMA model
arima_model <- auto.arima(ts_data)

# Print model summary
summary(arima_model)

# Plot the original data and fitted values
plot(ts_data, main = "Original Data and ARIMA Fit")
lines(fitted(arima_model), col = "red")

# Forecast future values (e.g., next 12 periods)
forecast_result <- forecast(arima_model, h = 12)

# Plot the forecast
plot(forecast_result, main = "ARIMA Forecast")

# Print forecast values
print(forecast_result)