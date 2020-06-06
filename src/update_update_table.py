from util_functions.athena_queries import AthenaQueries
q = AthenaQueries()
def lambda_handler(event, context):
    sql = """
    INSERT INTO default.kv_object_updates
    SELECT id, min(date(partition_2)) AS date_added
    FROM objects
    GROUP BY  1
    HAVING min(date(partition_2)) >= current_date - interval '1' day AND count(*) = 1 
    """
    print("Executing query")
    df = q.athena_query(sql)

def main():
    lambda_handler({},{})

if __name__ == "__main__":
    main()












