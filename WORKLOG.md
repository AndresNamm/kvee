# 2020-05-27 


~~~
CREATE EXTERNAL TABLE IF NOT EXISTS kv_object_updates
( 
  id STRING,
  lng STRING,
  lat STRING,
  dt DATE
) LOCATION 's3://kv-analysis/kv_object_updates';
~~~

# SOURCES 

+ [BAR PLOTS WITH STACKED PLUS CLUSTERED VIES](https://github.com/plotly/plotly.js/issues/1835)