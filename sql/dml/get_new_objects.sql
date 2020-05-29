INSERT INTO kv_object_updates
SELECT id, min(date(partition_2)) AS date_added
FROM objects
GROUP BY  1
HAVING min(date(partition_2)) >= current_date - interval '1' day AND count(*) = 1 