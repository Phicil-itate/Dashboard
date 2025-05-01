import os
import sys
from pathlib import Path
import argparse

# Add the current directory to path to import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from create_table_from_csv import create_table_from_csv
from csv_ingest import ingest_patient_csv_to_db

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Patient CSV Ingestion Pipeline')
    parser.add_argument('-c', '--csv', help='Path to the CSV file', default=None)
    parser.add_argument('-d', '--db', help='Path to the SQLite database', default=None)
    parser.add_argument('-t', '--table', help='Name of the table', default='Patient_interview')
    parser.add_argument('--create-only', action='store_true', help='Only create the table, do not ingest data')
    parser.add_argument('--ingest-only', action='store_true', help='Only ingest data, do not create the table')
    
    args = parser.parse_args()
    
    # Get the base directory of the script
    base_dir = Path(__file__).parent
    
    # Path to the CSV file
    csv_file_path = args.csv if args.csv else os.path.join(base_dir, 'csv', 'patient.csv')
    
    # Path to the SQLite database
    db_path = args.db if args.db else os.path.join(base_dir.parent, 'dashboard.db')
    
    # Create directory for the database if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    
    print(f"Using CSV file: {csv_file_path}")
    print(f"Using database: {db_path}")
    print(f"Using table: {args.table}")
    
    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return 1
    
    # Create the table if needed
    if not args.ingest_only:
        print("Creating table schema from CSV...")
        create_table_from_csv(csv_file_path, db_path, args.table)
    
    # Ingest the data if needed
    if not args.create_only:
        print("Ingesting CSV data into the database...")
        record_count = ingest_patient_csv_to_db(csv_file_path, db_path)
        print(f"Ingestion completed. {record_count} records processed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
