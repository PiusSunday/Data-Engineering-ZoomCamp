import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Use the container's dataset directory
    dataset_dir = '/app/dataset'
    # dataset_dir = "/Users/sunnythesage/PythonProjects/Data-Engineering-BootCamp/01 - docker-terraform/homework-1/src/dataset"
    os.makedirs(dataset_dir, exist_ok = True)

    # Determine the name of the output file based on the URL
    if url.endswith('.csv.gz'):
        csv_name = os.path.join(dataset_dir, 'gttr_output.csv.gz')
    else:
        csv_name = os.path.join(dataset_dir, 'gttr_output.csv')

    # Download the file using wget
    os.system(f"wget {url} -O {csv_name}")

    # Create a SQLAlchemy engine for PostgreSQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read the CSV file in chunks
    df_iter = pd.read_csv(csv_name, iterator = True, chunksize = 100000)

    df = next(df_iter)

    # Convert datetime columns to pandas datetime
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Write the first chunk to the database
    df.head(n = 0).to_sql(name = table_name, con = engine, if_exists = 'replace')

    # Append the first chunk to the database
    df.to_sql(name = table_name, con = engine, if_exists = 'append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)

            # Convert datetime columns to pandas datetime
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            # Append the chunk to the database
            df.to_sql(name = table_name, con = engine, if_exists = 'append')

            t_end = time()
            print('Inserted another chunk, took %.3f seconds' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the PostgreSQL database")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Ingest CSV data to Postgres')

    parser.add_argument('--user', required = True, help = 'user name for postgres')
    parser.add_argument('--password', required = True, help = 'password for postgres')
    parser.add_argument('--host', required = True, help = 'host for postgres')
    parser.add_argument('--port', required = True, help = 'port for postgres')
    parser.add_argument('--db', required = True, help = 'database name for postgres')
    parser.add_argument('--table_name', required = True, help = 'name of the table where we will write the results to')
    parser.add_argument('--url', required = True, help = 'url of the csv file')

    args = parser.parse_args()

    main(args)
