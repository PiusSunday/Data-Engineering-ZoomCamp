import os
import pandas as pd
from sqlalchemy import create_engine

# Define the path to the dataset folder
dataset_folder = '/Users/sunnythesage/PythonProjects/Data-Engineering-BootCamp/01 - docker-terraform/1_docker_postgresql/src/dataset'
csv_file_path = os.path.join(dataset_folder, 'taxi_zone_lookup.csv')

# Step 1: Read the CSV file
df_zones = pd.read_csv(csv_file_path)

# Step 2: Display the first few rows of the DataFrame (optional)
print("Data from CSV:")
print(df_zones.head(10))

# Database connection details
db_config = {
    "host": "localhost",  # Use the container name
    "port": 5434,  # PostgreSQL port inside the container
    "database": "gttr_2019_db",  # Database name
    "user": "postgres",  # Database user
    "password": "postgres"  # Database password
}

# Create the connection string
connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Ingest the data into the database
try:
    df_zones.to_sql("zones", con = engine, if_exists = "replace", index = False)
    print("Data successfully ingested into the database.")
except Exception as e:
    print(f"An error occurred: {e}")
