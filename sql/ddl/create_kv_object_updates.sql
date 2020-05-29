CREATE EXTERNAL TABLE kv_object_updates(
  id string, 
  date_added date)
LOCATION
  's3://kv-analysis/kv_object_updates'