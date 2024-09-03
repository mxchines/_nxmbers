import os
import pandas as pd
from datetime import datetime
from path_utility import get_data_path

def clean_data():
    # Define the input directory
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'nxmbers', 'data', 'csv')

    # Define the output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'nxmbers', 'data', 'cleaned')

    # Iterate over the CSV files in the input directory
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            # Construct the full file path
            input_file_path = os.path.join(input_dir, file)

            # Generate the timestamp
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

            # Define the output file name
            output_file_name = f'cleaned_{file}'
            output_file_path = os.path.join(output_dir, output_file_name)

            # Load the combined market data
            df = pd.read_csv(input_file_path)

            # Step 1: Standardize column names (lowercase and replace spaces with underscores)
            df.columns = df.columns.str.lower().str.replace(' ', '_')

            # Step 2: Remove any duplicate rows
            df = df.drop_duplicates()

            # Step 3: Handle missing values
            df = df.fillna('Unknown')  # Example to fill categorical columns with 'Unknown'

            # Step 4: Convert date columns to datetime format
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            # Step 5: Remove any rows where critical columns are missing (e.g., price, volume)
            df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])

            # Step 6: Save the cleaned data to a new CSV file
            df.to_csv(output_file_path, index=False)

            print(f"Data cleaning complete for {file}. Cleaned data saved to {output_file_path}.")

    # Import and run RDS uploader
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_storage'))
    from rds_uploader import main as rds_uploader_main
    rds_uploader_main()

if __name__ == "__main__":
    clean_data()