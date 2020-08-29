import logging
from util_functions.send_email import send_info_email
import os
from typing import Final
from util_functions.athena_queries import AthenaQueries
import json
#sd
WRITE_TO_LOCAL_CSV=False
WRITE_TO_S3=True

env=os.getenv('ENVIRONMENT','dev')
log_level: Final[str] = os.getenv('LOGLEVEL', 'INFO')
logging.getLogger(__name__).setLevel(log_level)
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)
q = AthenaQueries()


alarm_basis = {'Rakvere-1': {'cnt': 9}, 'Rakvere-2': {'cnt': 28}, 'Rakvere-3': {'cnt': 19}, 'Rakvere-4': {'cnt': 2}, 'Tallinn-1': {'cnt': 719}, 'Tallinn-2': {'cnt': 1399}, 'Tallinn-3': {'cnt': 1043}, 'Tallinn-4': {'cnt': 409}, 'Tallinn-5': {'cnt': 70}, 'Tartu-1': {'cnt': 157}, 'Tartu-2': {'cnt': 334}, 'Tartu-3': {'cnt': 291}, 'Tartu-4': {'cnt': 109}, 'Tartu-5': {'cnt': 9}}

def perform_tests():
        query = 'SELECT * from "dbt"."yesterday_count"'
        df = q.athena_query(query)
        df['index'] =  df['city'].str.cat(df['room_nr'],"-")
        city_counts=df[['index','cnt']].set_index('index').to_dict('index')
        fail=False
        for k,v in city_counts.items():
            if (v['cnt'] < alarm_basis[k]['cnt']):
                fail=True
        if fail:
            send_info_email(json.dumps(city_counts),'ERROR')
            
        if not fail:
            query2= 'SELECT * from "dbt"."example_data"'
            df = q.athena_query(query2)
            data=df.to_html()
            send_info_email(data, 'EXAMPLE DATASET')

def lambda_handler(event, context):
    perform_tests()


def main():
    e={}
    c=""
    lambda_handler(e,c)

if __name__ == "__main__":
    main()

