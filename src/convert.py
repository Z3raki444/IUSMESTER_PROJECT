# Import necessary libraries
import pandas as pd  # For reading CSV files and working with dataframes
from sqlalchemy import create_engine  # For database connection and SQL operations
import os  # For interacting with the operating system (e.g., file paths)

# Print the current working directory to help debug any file path issues
print("Current working directory:", os.getcwd())

# Define the SQLite database connection URL
database_url = "sqlite:///database.db"
engine = create_engine(database_url)  # Create a SQLAlchemy engine to connect to the SQLite database

# Define mapping of CSV filenames to their respective SQL table names
csv_to_table_map = {
    "train.csv": "train_table",
    "ideal.csv": "ideal_table",
    "test.csv": "test_table"
}

# Specify the directory where CSV files are stored
csv_directory = "datasets"  # Assumes a subdirectory named 'datasets' contains the CSV files

# Loop through each CSV file and corresponding table name
for csv_file, table_name in csv_to_table_map.items():
    # Construct the full path to the CSV file
    csv_path = os.path.join(csv_directory, csv_file)
    print(f"Checking for file at: {csv_path}")  # Print path for debugging

    # Check if the file exists before attempting to load it
    if os.path.exists(csv_path):
        print(f"Processing {csv_file} -> {table_name}")
        
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # Write the DataFrame to the SQLite database (replace table if it already exists)
        df.to_sql(table_name, engine, index=False, if_exists="replace")
        
        # Confirm successful insertion
        print(f"✔️  {table_name} created in database.db")
    else:
        # Inform the user if the file does not exist
        print(f"❌ File not found: {csv_path}")
