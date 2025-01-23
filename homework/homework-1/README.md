### Question 1:

docker run -it python:3.12.8 bash
root@908269d6afbf:/# pip list
Package Version
------- -------
pip     24.3.1
root@908269d6afbf:/# exit()


# *****************************************************************

### Question 2:

mkdir -p "$(pwd)/dataset"

##### BUILD THE IMAGE FOR THE DATA

docker build -t gttr_data_ingester:v01 .

##### INGEST THE DATA INTO THE DATABASE

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




# *****************************************************************


### Question 3:

#### 1.
SELECT
	count(trip_distance) 
FROM
	gttr_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' 
AND lpep_pickup_datetime < '2019-11-01'
AND lpep_dropoff_datetime >= '2019-10-01' 
AND lpep_dropoff_datetime < '2019-11-01'
AND trip_distance <= 1;

#### 2.
SELECT
	count(trip_distance) 
FROM
	gttr_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
	AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01'
AND
	trip_distance > 1 AND trip_distance <= 3;

#### 3:
SELECT
	count(trip_distance) 
FROM
	gttr_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
	AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01'
AND
	trip_distance > 3 AND trip_distance <= 7;

#### 4:
SELECT
	count(trip_distance) 
FROM
	gttr_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
	AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01'
AND
	trip_distance > 7 AND trip_distance <= 10;

#### 5:
SELECT
	count(trip_distance) 
FROM
	gttr_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
	AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01'
AND
	trip_distance > 10;


# *****************************************************************


### Question 4:

SELECT
    DATE(lpep_pickup_datetime) AS pickup_date,
    MAX(trip_distance) AS max_trip_distance
FROM
    gttr_data
WHERE
    lpep_pickup_datetime >= '2019-10-01' 
    AND lpep_pickup_datetime < '2019-11-01'
GROUP BY
    DATE(lpep_pickup_datetime)
ORDER BY
    max_trip_distance DESC
LIMIT 1;



# *****************************************************************


#### Question 5:

SELECT
    z."Zone",
    SUM(t."total_amount") AS total_amount
FROM
    gttr_data t
JOIN
    zones z ON t."PULocationID" = z."LocationID"
WHERE
    DATE(t."lpep_pickup_datetime") = '2019-10-18'
GROUP BY
    z."Zone"
HAVING
    SUM(t."total_amount") > 13000
ORDER BY
    total_amount DESC
LIMIT 3;



# *****************************************************************


#### question 6:

SELECT
    z."Zone",
    SUM(t."tip_amount") AS total_tip
FROM
    gttr_data t
JOIN
    zones z ON t."DOLocationID" = z."LocationID"
WHERE
    DATE(t."lpep_pickup_datetime") >= '2019-10-01'
    AND DATE(t."lpep_pickup_datetime") < '2019-11-01'
    AND t."PULocationID" = (SELECT "LocationID" FROM zones WHERE "Zone" = 'East Harlem North')
    AND z."Zone" IN ('Yorkville West', 'JFK Airport', 'East Harlem North', 'East Harlem South')
GROUP BY
    z."Zone"
ORDER BY
    total_tip DESC
LIMIT 1;

# ********

SELECT
    z."Zone",
    SUM(t."tip_amount") AS total_tip
FROM
    gttr_data t
JOIN
    zones z ON t."DOLocationID" = z."LocationID"
WHERE
    DATE(t."lpep_pickup_datetime") >= '2019-10-01'
    AND DATE(t."lpep_pickup_datetime") < '2019-11-01'
    AND t."PULocationID" = (SELECT "LocationID" FROM zones WHERE "Zone" = 'East Harlem North')
    AND z."Zone" IN ('Yorkville West', 'JFK Airport', 'East Harlem North', 'East Harlem South')
GROUP BY
    z."Zone"
ORDER BY
    total_tip DESC;
