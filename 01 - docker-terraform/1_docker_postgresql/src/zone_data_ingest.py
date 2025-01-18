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

# Step 3: Create a SQLAlchemy engine to connect to PostgreSQL
# Replace the following with your actual connection details
user = 'root'
password = 'root'
host = 'localhost'  # Use the service name defined in your docker-compose
port = '5432'
db = 'nyc_tlc_trd'

# Create the SQLAlchemy engine
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

# Step 4: Import the DataFrame into PostgreSQL
try:
    df_zones.to_sql(name = 'zones', con = engine, if_exists = 'replace', index = False)
    print("Data imported successfully into the 'zones' table.")
except Exception as e:
    print(f"An error occurred: {e}")
