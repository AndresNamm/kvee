import numpy as np
import collections
import csv
import logging
import os
from requests_html import HTMLSession
from typing import List
from requests_html import HTMLSession
import requests
import collections
import logging
import numpy
import os
from pathlib import Path
from datetime import date
import logging.config
import time
import json
from util_functions.athena_queries import AthenaQueries
import time
from random import randrange
import util_functions.s3_utils as s3_utils
import random
import string 
from datetime import datetime
q = AthenaQueries()




map_names = {'id': 'id',
 'Müüa korter': 'title',
 'Tube': 'room_nr',
 'Üldpind': 'total_size',
 'Korrus/Korruseid': 'floor_inf',
 'Ehitusaasta': 'build_year',
 'Seisukord': 'status',
 'Omandivorm': 'ownership_form',
 'Energiamärgis': 'energy',
 'raw_data': 'raw',
 'Katastrinumber': 'cataster',
 'Anda üürile korter': 'title',
 'Kulud suvel/talvel': 'expenses_summer_winter',
 'Müüa korter, Vahetuse võimalus': 'title',
 'Müüa korter (Broneeritud)': 'title',
 'Anda üürile korter (Broneeritud)': 'title',
 'Kinnistu number': 'property_nr',
 'Korruseid': 'total_floors'}

env=os.getenv('ENVIRONMENT','dev')
external_log_level=os.getenv('EXTERNAL_LOG_LEVEL','INFO')
internal_log_level=os.getenv('INTERNAL_LOG_LEVEL','DEBUG')
logging.basicConfig(level=external_log_level)
logging.getLogger(__name__).setLevel(internal_log_level)
logger = logging.getLogger(__name__)


# def dict_list_to_df(dlist):
#     res = {v:[]  for v in map_names.values()}
#     for element in dlist: 
#         for k,v in res.items():
#             temp_val = element[k] if k in element else None
#             v.append(temp_val)
#     df = pd.DataFrame(res)
#     return df

def map_table_names(table):
    res={}
    for k,v in table.items():
        new_name=map_names[k]
        res[new_name]=v
    return res

def get_object_details_info(object_id):
    try:
        session = HTMLSession()
        address=f"https://www.kv.ee/index.php?act=object.show&object_id={object_id}"
        logger.info(f"Scraping {object_id}")
        r = session.get(address)    
        res = r.html.find('div.object-article-details',first=True)
        col=res.find('th')
        val=res.find('td')
        table = {}
        for i in range(len(col)-1):
            table[col[i+1].text]=val[i].text
        res2 = r.html.find('div.object-article-section',first=False)
        lst = [ i.html for i in res2]
        todays_date=datetime.today().strftime('%Y-%m-%d')
        return {"id":object_id, **map_table_names(table) ,"raw_data":lst,"date_added":todays_date}
    except: 
        return {"id":object_id}

def read_in_objects(limit=100):
    sql = f"SELECT id FROM default.kv_get_objects_to_update LIMIT {limit}"
    res = q.athena_query(sql)
    return res["id"].tolist()

def add_scraper_objects(lst):
    bucketname="kv-analysis"
    rnd = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    todays_date=datetime.today().strftime('%Y-%m-%d')
    s3_utils.s3_put_rows(list(map(lambda kv_obj: json.dumps(kv_obj),lst)),bucketname,f"object_info/{rnd}-kv.json")
    s3_utils.s3_put_rows(list(map(lambda kv_obj: json.dumps({"id":kv_obj["id"],"date_added":todays_date}),lst)),bucketname,f"kv_object_updates/{rnd}-kv.json")


def main(object_count=4):
    res = []
    for obj in read_in_objects(object_count):
        all_details = get_object_details_info(obj)
        res.append(all_details)
        
    add_scraper_objects(res)
    
def lambda_handler(event, context):
    logger.info("Start execution")
    object_count=10
    if "object_count" in event:
        object_count=event["object_count"]
    main(object_count=object_count)

if __name__ == "__main__":
    main()








