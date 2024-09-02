import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
from path_utility import get_data_path
from tqdm import tqdm  # Importing tqdm for the progress bar

# Database connection parameters
DB_HOST = "numbermxchine.cxwoaq8ccu34.eu-west-2.rds.amazonaws.com"
DB_NAME = "nxmbers"
DB_USER = "mxchinist"
DB_PASS = "foJzyn-miwhor-bavpo4"
DB_PORT = "5432"

def create_table_name():
    """Create a table name with current date."""
    return f"market_data_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}"

def get_column_types(df):
    """Map pandas dtypes to PostgreSQL column types."""
    type_mapping = {
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'object': 'TEXT',
        'datetime64[ns]': 'TIMESTAMP'
    }
    return {col: type_mapping.get(str(df[col].dtype), 'TEXT') for col in df.columns}

def create_table(conn, cursor, table_name, column_types):
    """Create a new table in the database."""
    columns = [
        sql.SQL("{} {}").format(
            sql.Identifier(col),
            sql.SQL(col_type)
        ) for col, col_type in column_types.items()
    ]

    create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(columns)
    )

    cursor.execute(create_table_query)
    conn.commit()

def insert_data(conn, cursor, table_name, df):
    """Insert data into the table."""
    columns = list(df.columns)
    values = [tuple(x) for x in df.to_numpy()]

    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )

    for value in tqdm(values, desc="Inserting data"):
        cursor.execute(insert_query, value)
    conn.commit()

def upload_to_rds(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Ensure 'date' column is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Connect to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Create table name
    table_name = create_table_name()

    # Get column types
    column_types = get_column_types(df)

    # Create table
    create_table(conn, cursor, table_name, column_types)

    # Insert data
    insert_data(conn, cursor, table_name, df)

    print(f"Data successfully inserted into table: {table_name}")

    # Close connection
    cursor.close()
    conn.close()

    return table_name

def main():
    # Define the directory containing the cleaned CSV files
    cleaned_dir = os.path.join(os.path.dirname(__file__), '..', 'nxmbers', 'data', 'cleaned')

    # Iterate over the cleaned CSV files
    for file in os.listdir(cleaned_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(cleaned_dir, file)
            print(f"Uploading {file} to RDS...")
            upload_to_rds(file_path)

if __name__ == "__main__":
    main()