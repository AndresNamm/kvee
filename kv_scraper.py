from typing import List
from requests_html import HTMLSession
import requests
import collections
import logging
import numpy
import src.scraper_utils as scraper_utils
import src.s3_utils as s3_utils
from src.models import KvObject,KvObjectDetails,City
import os
from pathlib import Path
from datetime import date
import logging.config
import time
import json

#sd

WRITE_TO_LOCAL_CSV=False
WRITE_TO_S3=True

env=os.getenv('ENVIRONMENT','dev')
external_log_level=os.getenv('EXTERNAL_LOG_LEVEL','INFO')
internal_log_level=os.getenv('INTERNAL_LOG_LEVEL','DEBUG')
logging.basicConfig(level=external_log_level)
logging.getLogger(__name__).setLevel(internal_log_level)
logger = logging.getLogger(__name__)

# TODO: set this up somewhere els
#logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
#logging.debug("debug")


class KVBuilder:
    def __init__(self):
        self.session = HTMLSession()

    def format_object_url(self,deal_type,county,parish,rooms):
        object_uri = f"https://www.kv.ee/?act=search.objectcoords&deal_type={deal_type}&page=1&orderby=ob&page_size=100000&search_type=new&county={county}&parish={parish}&zoom=25&rooms_min={rooms}&rooms_max={rooms}"
        return  object_uri

    def get_object_details(self, kv_object,city,room_nr):
        cnt=0
        received=False
        while cnt < 15 or received:
            try :
                object_id=kv_object.id
                address='https://kv.ee/?act=search.objectinfo&object_id={}'.format(object_id)
                r = self.session.get(address)
                received=True
                try:
                    details=scraper_utils.parse_details_from_html( r )
                    result = KvObjectDetails(id=object_id,lng=kv_object.lng, lat = kv_object.lat, abs_size= details['absolute_size'], abs_price= details['absolute_price'],name = city.name, county = city.county, parish = city.parish, title=details['title'], room_nr=room_nr)
                    return result
                except Exception as e:
                    logger.error( f"Download failure url: {address}" )
                    logger.error( e )
                    logger.error( r.text )
            except Exception as e:
                logger.error(e)
                cnt+=1
                logger.error(f"Trying {cnt} time")
                time.sleep(3)

    def fetch_city_objects(self,city, room_nr,deal_type=1):
        url=self.format_object_url(deal_type=deal_type,county = city.county,parish = city.parish,rooms= room_nr)
        logger.info(url)
        kv_json_response = requests.get(url).json()
        logger.debug(kv_json_response)
        kv_objects: List[KvObject]=scraper_utils.handle_search_results( kv_json_response, city )
        kv_object_details:List[KvObjectDetails]=list(map(lambda kv_object: self.get_object_details(kv_object=kv_object,city=city,room_nr = room_nr),kv_objects))
        return (kv_objects,kv_object_details)
        
def main(city_name="rakvere",deal_type="all",room_nr=1):
    kv = KVBuilder()
    
    # INITIAL CONFIGURATION FOR DOWNLOAD
    # TODO: to ssm 
    rakvere=City(name="Rakvere",county=7,parish=1050)
    tallinn=City(name="Tallinn",county=1,parish=1061)
    tartu=City(name="Tartu",county=12,parish=1063)
    deals={1:"sale",2:"rent"}
    cities_k={"rakvere":rakvere,"tartu":tartu,"tallinn":tallinn}
    # PARAMETER PARSING 
    if city_name=="":
        cities=[rakvere]
    elif city_name=="all":
        cities=[rakvere,tartu,tallinn]
    else:
        cities=[cities_k[city_name]]

    if deal_type!="all":
        deal_types=[deal_type]
    else:
        deal_types=[1,2]
        
    today=date.today().strftime("%Y-%m-%d")
    if(room_nr=="all"):
        room_sizes=[1,2,3,4,5]
    else:
        room_sizes=[room_nr]


    # ACTUAL DOWNLOAD
    # improve based on
    # FOR DEAL TYPE  energy_certs=A,B,C,D,E,F
    # FOR c%5B%5D=800 = uusarendus
    #keyword_dev_type="c%5B%5D"
    #dev_type={800:"uusarendus",38}
    for deal_type in deal_types:
        for city in cities:
            for room_size in room_sizes :
                obj = [ ]
                det = [ ]
                logger.info(f"Fetching city named {city.name} with deal type {deal_type} and room_size {room_size}")
                obj,det = kv.fetch_city_objects( city, deal_type=deal_type, room_nr = room_size)
                logger.info("Object results are downloaded")  
                if WRITE_TO_S3:
                    bucketname=f"{env}-kinnisvara-etl-raw-data-daily-incremental"
                    objects_key=f"objects/{deals[deal_type]}/{city.name}/{today}/{room_size}/kv_objects.json"
                    object_details_key=f"details/{deals[deal_type]}/{city.name}/{today}/{room_size}/kv_objects_details.json"
                    s3_utils.s3_put_rows(list(map(lambda kv_obj: json.dumps(kv_obj.__dict__),obj)),bucketname,objects_key)
                    #s3_utils.s3_put_dict(list(map(lambda kv_obj: kv_obj.__dict__,obj)),bucketname,object_details_key)
                    logger.info(f"Stored objects to S3 s3://{bucketname}/{objects_key}")
                    #s3_utils.s3_put_dict(list(map(lambda kv_obj_det: kv_obj_det.__dict__,det)),bucketname,object_details_key)
                    s3_utils.s3_put_rows(list(map(lambda kv_obj_det: json.dumps(kv_obj_det.__dict__),det)),bucketname,object_details_key)
                    logger.info(f"Stored object details to S3 s3://{bucketname}/{object_details_key}")

def lambda_handler(event, context):
    city_name=event["city_name"]
    deal_type=event["deal_type"]
    room_nr=event["room_nr"]
    main(city_name,deal_type,room_nr)

if __name__ == "__main__":
    main()

