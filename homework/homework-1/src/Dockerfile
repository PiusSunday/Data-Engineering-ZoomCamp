FROM python:3.12

LABEL authors="sunnythesage"

# Install wget and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install pandas pyarrow sqlalchemy psycopg2-binary

WORKDIR /app
COPY gttr_data_ingest.py gttr_data_ingest.py

ENTRYPOINT [ "python", "gttr_data_ingest.py" ]