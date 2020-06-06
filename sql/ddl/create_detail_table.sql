CREATE EXTERNAL TABLE object_detailed (
id STRING,
title STRING,
room_nr STRING,
total_size STRING,
floor_inf STRING,
build_year STRING,
status STRING,
ownership_form STRING,
energy STRING,
raw STRING,
cataster STRING,
expenses_summer_winter STRING,
property_nr STRING,
total_floors STRING
 )
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://kv-analysis/object_info/';