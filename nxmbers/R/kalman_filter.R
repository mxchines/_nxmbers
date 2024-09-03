import numpy as np
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def kalman_filter(data, initial_state, process_noise_variance, measurement_noise_variance):
    """
    Implements a basic Kalman filter for time series data.

    Args:
        data: A 1D numpy array containing the time series data.
        initial_state: A tuple (x0, P0) representing the initial state estimate and its covariance.
        process_noise_variance: The variance of the process noise (Q).
        measurement_noise_variance: The variance of the measurement noise (R).

    Returns:
        filtered_state_means: A 1D numpy array containing the filtered state estimates.
        filtered_state_covariances: A 1D numpy array containing the filtered state covariances.
    """

    # Extract initial state estimate and covariance
    x, P = initial_state

    # Initialize lists to store filtered state means and covariances
    filtered_state_means = []
    filtered_state_covariances = []

    # Kalman filter iterations
    for z in data:
        # Prediction step
        x_pred = x  # State prediction (assuming a simple random walk model)
        P_pred = P + process_noise_variance

        # Update step
        K = P_pred / (P_pred + measurement_noise_variance)  # Kalman gain
        x = x_pred + K * (z - x_pred)  # State update
        P = (1 - K) * P_pred  # Covariance update

        # Store filtered state mean and covariance
        filtered_state_means.append(x)
        filtered_state_covariances.append(P)

    return np.array(filtered_state_means), np.array(filtered_state_covariances)

# ... (your existing code for data fetching and preprocessing) ...

# Apply Kalman filter
initial_state = (pdf['close_alpha'].iloc[0], 1.0)  # Initial state estimate and covariance
process_noise_variance = 0.1  # Adjust based on your understanding of the process
measurement_noise_variance = 1.0  # Adjust based on your understanding of the measurement noise

filtered_state_means, filtered_state_covariances = kalman_filter(
    pdf['close_alpha'].values, initial_state, process_noise_variance, measurement_noise_variance
)

# Plot the filtered results
logging.info("Plotting Kalman filtered results...")
plt.figure(figsize=(12, 6))
plt.plot(pdf['date'], pdf['close_alpha'], label='Actual')
plt.plot(pdf['date'], filtered_state_means, label='Kalman Filtered', color='green')
plt.title('Kalman Filter Results')
plt.xlabel('Date')
plt.ylabel('Close Alpha')
plt.legend()
plt.savefig('../nxmbers/data/plots/png/kalman_filter_plot.png')

logging.info("Kalman filter analysis complete! Plot saved as kalman_filter_plot.png")