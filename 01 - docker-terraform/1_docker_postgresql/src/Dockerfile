#FROM python:3.12
#
#LABEL authors="sunnythesage"
#
#RUN pip install pandas, pyarrow
#
#WORKDIR /app
#COPY pipeline.py pipeline.py
#
#ENTRYPOINT [ "python", "pipeline.py" ]

# **************************************************

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
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
