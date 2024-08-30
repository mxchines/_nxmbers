import os
import pandas as pd
from datetime import datetime
from path_utility import get_data_path

def clean_data():
    # Define the input path
    input_file_path = get_data_path(__file__, 'combined_data.csv')

    # Generate the timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Define the directory and the file name
    output_dir = os.path.join(os.getcwd(), '..', 'nxmbers', 'data', 'cleaned')  
    output_file_name = f'cleaned_data-{timestamp}.csv'
    output_file_path = os.path.join(output_dir, output_file_name)

    # Load the combined market data
    df = pd.read_csv(input_file_path)

    # Step 1: Standardize column names (lowercase and replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Step 2: Remove any duplicate rows
    df = df.drop_duplicates()

    # Step 3: Handle missing values
    # Here are a few approaches. You can uncomment the one you want to use:

    # Option 1: Drop rows with any missing values
    # df = df.dropna()

    # Option 2: Fill missing values with a specific value (e.g., 0, 'Unknown', etc.)
     df = df.fillna(NaN)  # Example to fill numeric columns with 0
     df = df.fillna('Unknown')  # Example to fill categorical columns with 'Unknown'

    # Option 3: Fill missing values with the mean/median/mode for numeric columns
    # df = df.fillna(df.mean())  # Fill with mean
    # df = df.fillna(df.median())  # Fill with median
    # df = df.apply(lambda x: x.fillna(x.mode()[0]) if x.dtype == 'O' else x, axis=0)  # Fill with mode for categorical

    # Step 4: Convert date columns to datetime format
    # If you have date columns, convert them using the following line:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Step 5: Remove any rows where critical columns are missing (e.g., price, volume)
    df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])

    # Step 6: Save the cleaned data to a new CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Data cleaning complete. Cleaned data saved to {output_file_path}.")
    
    return output_file_path

if __name__ == "__main__":
    clean_data()