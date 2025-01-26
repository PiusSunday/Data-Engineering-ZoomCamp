# Data Engineering ZoomCamp - Module 1 Homework

## Overview

This repository contains solutions for Module 1 Homework, focusing on Docker and SQL. The homework involves working with
Docker containers, setting up a PostgreSQL database, and performing data analysis on Green Taxi Trip Records data.

## Technologies Used

- Docker
- PostgreSQL
- SQL
- Terraform
- PyCharm

## Homework Setup and Solutions

### Question 1: Docker Image and pip Version

**Objective**: Run a Python Docker image and check pip version

**Command**:

```bash
docker run -it python:3.12.8 bash

root@908269d6afbf:/# pip list
```

**Result**:

- pip 24.3.1

### Question 2: Docker Networking and docker-compose

In Docker Compose, services can communicate with each other using their service names as hostnames. The pgadmin service
should connect to the db service using the following details:

**Hostname**: **db** (the service name of the PostgreSQL container)

**Port**: **5432** (the internal PostgreSQL port inside the container)

### Question 3: Trip Segmentation Count

SQL queries to count trips by distance ranges for October 2019:

1. Up to 1 mile
2. Between 1 and 3 miles
3. Between 3 and 7 miles
4. Between 7 and 10 miles
5. Over 10 miles

**The following SQL queries calculate the number of trips for each segment**:

#### 1. Up to 1 mile

```sql
SELECT COUNT(trip_distance)
FROM gttr_data
WHERE lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime < '2019-11-01'
  AND trip_distance <= 1;
```

#### 2. Between 1 and 3 miles

```sql
SELECT COUNT(trip_distance)
FROM gttr_data
WHERE lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime < '2019-11-01'
  AND trip_distance > 1
  AND trip_distance <= 3;
```

#### 3. Between 3 and 7 miles

```sql
SELECT COUNT(trip_distance)
FROM gttr_data
WHERE lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime < '2019-11-01'
  AND trip_distance > 3
  AND trip_distance <= 7;
```

#### 4. Between 7 and 10 miles

```sql
SELECT COUNT(trip_distance)
FROM gttr_data
WHERE lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime < '2019-11-01'
  AND trip_distance > 7
  AND trip_distance <= 10;
```

#### 5. Over 10 miles

```sql
SELECT COUNT(trip_distance)
FROM gttr_data
WHERE lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime < '2019-11-01'
  AND trip_distance > 10;
```

### Question 4: Longest Trip per Day

**The following SQL query identifies the pickup day with the longest trip distance**:

```sql
SELECT
    DATE (lpep_pickup_datetime) AS pickup_date, MAX (trip_distance) AS max_trip_distance
FROM
    gttr_data
WHERE
    lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime
    < '2019-11-01'
GROUP BY
    DATE (lpep_pickup_datetime)
ORDER BY
    max_trip_distance DESC
    LIMIT 1;
```

### Question 5: Top Pickup Locations by Total Amount

**The following SQL query identifies the top pickup zones**:

```sql
SELECT z."Zone",
       SUM(t."total_amount") AS total_amount
FROM gttr_data t
         JOIN
     zones z ON t."PULocationID" = z."LocationID"
WHERE
    DATE (t."lpep_pickup_datetime") = '2019-10-18'
GROUP BY
    z."Zone"
HAVING
    SUM (t."total_amount")
     > 13000
ORDER BY
    total_amount DESC
    LIMIT 3;
```

### Question 6: Largest Tip for East Harlem North Pickups

The following SQL query identifies the drop-off zone with the largest tip:

```sql
SELECT z."Zone",
       SUM(t."tip_amount") AS total_tip
FROM gttr_data t
         JOIN
     zones z ON t."DOLocationID" = z."LocationID"
WHERE
    DATE (t."lpep_pickup_datetime") >= '2019-10-01'
  AND DATE (t."lpep_pickup_datetime")
    < '2019-11-01'
  AND t."PULocationID" = (SELECT "LocationID" FROM zones WHERE "Zone" = 'East Harlem North')
GROUP BY
    z."Zone"
ORDER BY
    total_tip DESC
    LIMIT 1;
```

### Question 7: Terraform Workflow

The correct sequence for the Terraform workflow is:

terraform init, terraform apply -auto-approve, terraform destroy

1. `terraform init`: Download provider plugins and set up backend.
2. `terraform apply -auto-approve`: Generate and execute proposed changes.
3. `terraform destroy`: Remove all resources managed by Terraform for the current configurations.

## Data Ingestion Process

##### Download the Datasets

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

### Docker Data Ingestion

##### BUILD THE IMAGE FOR THE DATA

```bash

docker build -t gttr_data_ingester:v01 .

```

##### To ingest the Green Taxi Trip Data to PostgreSQL and containerize it, I used the following commands based on my personal configurations:

```bash

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

docker run --rm \
  -v "$(pwd)/dataset:/app/dataset" \
  --network=pg-network-new \
  gttr_data_ingester:v01 \
  --user=postgres \
  --password=postgres \
  --host=pg-database-new \
  --port=5432 \
  --db=gttr_2019_db \
  --table_name=gttr_data \
  --url=${URL}
```
