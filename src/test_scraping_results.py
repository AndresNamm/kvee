import logging
from util_functions.send_email import send_info_email
import os
from typing import Final
from util_functions.athena_queries import AthenaQueries
import json
import pandas as pd
from datetime import date

#sd
WRITE_TO_LOCAL_CSV=False
WRITE_TO_S3=True

env=os.getenv('ENVIRONMENT','dev')
log_level: Final[str] = os.getenv('LOGLEVEL', 'INFO')
logging.getLogger(__name__).setLevel(log_level)
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)
q = AthenaQueries()


all_emails=["andres.namm.001@gmail.com","sigridmalinen@gmail.com", "jyrimalinen1@gmail.com", "annemalinen27@gmail.com", "jaan911@gmail.com", "rauno.naksi@gmail.com", "renartupits@gmail.com", "kyllike@namm.ee","andres.namm@namm.ee","mart.randala@gmail.com"]
main_man=["andres.namm.001@gmail.com"]
alarm_basis = {'Rakvere-1': {'cnt': 5}, 'Rakvere-2': {'cnt': 18}, 'Rakvere-3': {'cnt': 15}, 'Rakvere-4': {'cnt': 0}, 'Tallinn-1': {'cnt': 719}, 'Tallinn-2': {'cnt': 1399}, 'Tallinn-3': {'cnt': 1043}, 'Tallinn-4': {'cnt': 409}, 'Tallinn-5': {'cnt': 70}, 'Tartu-1': {'cnt': 157}, 'Tartu-2': {'cnt': 334}, 'Tartu-3': {'cnt': 291}, 'Tartu-4': {'cnt': 109}, 'Tartu-5': {'cnt': 2}}

def perform_tests():
        query = 'SELECT * from "dbt"."yesterday_count"'
        df = q.athena_query(query)
        df['index'] =  df['city'].str.cat(df['room_nr'],"-")
        city_counts=df[['index','cnt']].set_index('index').to_dict('index')
        fail=False
        for k,v in city_counts.items():
            if (v['cnt'] < alarm_basis[k]['cnt']):
                fail=True
        # 1 EMAIL
        if fail:
            send_info_email(json.dumps(city_counts),'ERROR')
        
        cities=['Tartu','Rakvere','Tallinn']
        if not fail:
            # 2 EMAIL
            query2= 'SELECT * from "dbt"."example_data"'
            df = q.athena_query(query2)
            data=df.to_html()
            send_info_email(data, 'EXAMPLE DATASET')
            full_df = pd.DataFrame()
            # 3 EMAIL
            for city in cities:
                query3= f"""SELECT concat('https://www.kv.ee/',id) as url,* FROM "dbt"."active_sale_highest_price_drops" where city = '{city}' order by diff_perc desc limit 20;"""
                df = q.athena_query(query3)
                full_df = pd.concat([full_df,df])
            data=full_df.to_html() 

            if date.today().weekday() == 6:
                send_info_email(data, 'Suurimad langetajad Tartu,Rakvere,Tallinn',all_emails)
            else:
                send_info_email(data, 'Suurimad langetajad Tartu,Rakvere,Tallinn',main_man)
 
            
def lambda_handler(event, context):
    perform_tests()


def main():
    e={}
    c=""
    lambda_handler(e,c)

if __name__ == "__main__":
    main()

