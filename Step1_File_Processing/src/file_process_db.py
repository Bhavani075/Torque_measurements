import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Folder paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Project root directory
RAW_FOLDER_PATH = BASE_DIR / 'Input/raw'           # Folder containing raw Excel files
CLEANED_FOLDER_PATH = BASE_DIR / 'Input/cleaned'   # Folder for cleaned files
DATABASE_NAME = 'trq_db'                           # Database name
DB_PATH = BASE_DIR / DATABASE_NAME                 # Path to the SQLite database file

# Function to create the SQLite database engine
def create_database_engine(db_path):
    if not db_path.exists():
        logging.warning(f"Database file does not exist at {db_path}. It will be created.")
    engine = create_engine(f"sqlite:///{db_path}")
    try:
        # Check if database connection is successful
        inspect(engine)
        logging.info(f"Database engine created and connected to {db_path}")
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise
    return engine

# Function to process Excel files
def process_excel_files():
    # Ensure raw and cleaned folders exist
    if not RAW_FOLDER_PATH.exists():
        raise FileNotFoundError(f"Raw folder does not exist: {RAW_FOLDER_PATH}. Please create it and add files to process.")
    CLEANED_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

    # Get the current date for table naming
    current_date = datetime.now().strftime('%Y%m%d')

    # Create database engine
    engine = create_database_engine(DB_PATH)

    try:
        # Iterate through all Excel files in the raw folder
        for file_name in os.listdir(RAW_FOLDER_PATH):
            if file_name.lower().endswith('.xlsx'):  # Process only Excel files
                file_path = RAW_FOLDER_PATH / file_name
                table_name = os.path.splitext(file_name)[0]  # Extract the file name without extension
                table_name_with_date = f"{table_name}_{current_date}"  # Append current date to table name

                logging.info(f"Processing file: {file_name}")

                try:
                    # Read the Excel file, skipping the first 49 rows and selecting columns A and B (time, torque)
                    df = pd.read_excel(file_path, skiprows=49, usecols=[0, 1], names=['time', 'torque'], engine='openpyxl')

                    # Write data to the database table
                    df.to_sql(table_name_with_date, con=engine, if_exists='replace', index=False)
                    logging.info(f"Data inserted into table: {table_name_with_date}")

                    # Save cleaned data to the 'cleaned' folder
                    cleaned_file_name = f"{table_name_with_date}.xlsx"
                    cleaned_file_path = CLEANED_FOLDER_PATH / cleaned_file_name
                    df.to_excel(cleaned_file_path, index=False)
                    logging.info(f"Cleaned file saved to: {cleaned_file_path}")

                    # Delete the original file from the raw folder
                    os.remove(file_path)
                    logging.info(f"Original file deleted: {file_path}")

                except Exception as e:
                    logging.error(f"Error processing '{file_name}': {e}")
    finally:
        # Close the database connection explicitly
        engine.dispose()
        logging.info("Database connection closed.")

# Run the script
if __name__ == "__main__":
    logging.info("Starting file processing...")
    try:
        process_excel_files()
        logging.info("File processing completed successfully.")
    except Exception as e:
        logging.error(f"Critical error: {e}")