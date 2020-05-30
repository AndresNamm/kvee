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
from util_functions.s3_utils import s3_put_dict
import random
import string 
from datetime import datetime
import pandas as pd
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


def dict_list_to_df(dlist):
    res = {v:[]  for v in map_names.values()}
    for element in dlist: 
        for k,v in res.items():
            temp_val = element[k] if k in element else None
            v.append(temp_val)
    df = pd.DataFrame(res)
    return df

def map_table_names(table):
    res={}
    for k,v in table.items():
        new_name=map_names[k]
        res[new_name]=v
    return res

def get_object_details_info(object_id):
    session = HTMLSession()
    address=f"https://www.kv.ee/index.php?act=object.show&object_id={object_id}"
    r = session.get(address)    
    res = r.html.find('div.object-article-details',first=True)
    col=res.find('th')
    val=res.find('td')
    table = {}
    for i in range(len(col)-1):
        table[col[i+1].text]=val[i].text
    res2 = r.html.find('div.object-article-section',first=False)
    lst = [ i.html for i in res2]
    return {"id":object_id, **map_table_names(table) ,"raw_data":lst}

def read_in_objects(limit=100):
    sql = f"SELECT id FROM default.kv_get_objects_to_update LIMIT {limit}"
    res = q.athena_query(sql)
    return res["id"].tolist()

def add_scraper_objects(lst):
    rnd = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    #s3_put_dict(lst,f"kv-analysis",f"object_info/{rnd}-kv.json")
    
    details = dict_list_to_df(lst)

    q.write_to_athena_table(details,'s3://kv-analysis/object_info/','object_detailed')
    todays_date=datetime.today()
    df = pd.DataFrame({"id":[i["id"] for i in lst], "date_added": [todays_date for i in range(len(lst))]})
    q.write_to_athena_table(df,"s3://kv-analysis/kv_object_updates/","kv_object_updates")

def main(object_count=4):
    res = []
    for obj in read_in_objects(object_count):
        all_details = get_object_details_info(obj)
        res.append(all_details)
    add_scraper_objects(res)
    
def lambda_handler(event, context):
    object_count=100
    if "object_count" in event:
        object_count=event["object_count"]
    main(object_count=100)

if __name__ == "__main__":
    main()








