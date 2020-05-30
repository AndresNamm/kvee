CREATE EXTERNAL TABLE kv_object_updates(
  id string, 
  date_added date)
STORED AS PARQUET
LOCATION
  's3://kv-analysis/kv_object_updates'
