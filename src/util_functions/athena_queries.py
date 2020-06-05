import pandas as pd
from pyathena import connect
#import awswrangler as wr

class AthenaQueries:

    def __init__(self,s3_staging_dir='s3://andresmb/Unsaved/'):
        self.conn = connect(s3_staging_dir=s3_staging_dir,
                            region_name='eu-west-1')

    def athena_query(self, query):
        df = pd.read_sql(query, self.conn)
        return df

    # GET AVERAGE ACTIVE TIME FOR apartments with certain room_nr in Rakvere,Tartu,Tallinn
    def get_avg_waiting_room_nr(self, deal_type, room_nr, min_stat=3, days_inactive=2):
        query = f"""
        with t1 as
        (SELECT city,room_nr,AVG(days_active) as avg_age ,count(*) as cnt FROM "default"."state_view"
        where days_inactive > {days_inactive} and deal_type = '{deal_type}' and room_nr = {room_nr} GROUP BY 1,2)
        SELECT * FROM t1 WHERE cnt > {min_stat};"""
        df = self.athena_query(query)
        return df

    def get_avg_wait_time(self, deal_type, min_stat=3, days_inactive=2):
        res = {}
        for room_nr in range(1, 6):
            res[room_nr] = self.get_avg_waiting_room_nr(
                deal_type, room_nr, min_stat, days_inactive)
        return res

    def get_price_differences(self, deal_type="sale"):
        query = f"""
        SELECT url,
         room_nr,
         title,
         partition_1,
         abs_size,
         abs_price,
         lag(abs_price,1) over(order by url,date(partition_2)) as prev_price,
         date(partition_2) AS dt
            FROM "default"."details"
            WHERE partition_0 = '{deal_type}'
        """
        df = self.athena_query(query)
        return df

    # def write_to_athena_table(self,df,path,table):
    #     wr.s3.to_parquet(
    #     df=df,
    #     path=path,
    #     dataset=True,
    #     database="default",
    #     table=table)
