CREATE EXTERNAL TABLE kv_object_updates(
  id string, 
  date_added date)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION
  's3://kv-analysis/kv_object_updates'
