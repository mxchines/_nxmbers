import pandas as pd

def clean_data(combined_data):
    """
    Cleans the combined DataFrame.

    Args:
        combined_data: The DataFrame containing combined data from Yahoo Finance and Alpha Vantage.

    Returns:
        The cleaned DataFrame.
    """

    # Check for missing values
    print(combined_data.isnull().sum())

    # Handle missing values (fill with previous valid value)
    combined_data.fillna(method='ffill', inplace=True)

    # Optional: Outlier detection and removal (example: Z-score method)
    # ... (Implement outlier detection and removal if needed)

    return combined_data