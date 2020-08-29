from typing import List,Final
from requests_html import HTMLSession
import requests
import collections
import logging
import numpy
import util_functions.scraper_utils as scraper_utils
import util_functions.s3_utils as s3_utils
from util_functions.models import KvObject,KvObjectDetails,City
import os
from pathlib import Path
from datetime import date
import logging.config
import time
import json
from dataclasses import dataclass,asdict
import time


#sd
WRITE_TO_LOCAL_CSV=False
WRITE_TO_S3=True

env=os.getenv('ENVIRONMENT','dev')
log_level: Final[str] = os.getenv('LOGLEVEL', 'INFO')

logging.getLogger(__name__).setLevel(log_level)
logger = logging.getLogger(__name__)
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

    def get_object_details(self, kv_object,city,room_nr)->KvObjectDetails:
        cnt=0
        while cnt < 15:
            try :
                object_id=kv_object.id
                address='https://kv.ee/?act=search.objectinfo&object_id={}'.format(object_id)
                r = self.session.get(address)
                received=True               
                try:
                    details=scraper_utils.parse_details_from_html(r)
                    result = KvObjectDetails(id=object_id,lng=kv_object.lng, lat = kv_object.lat, name = city.name, county = city.county, parish = city.parish,  room_nr=room_nr, **details)
                    return result
                except Exception as e:
                    logger.error( f"Parsing: {address}" )
                    logger.error(e)
                    return KvObjectDetails(id=object_id,lng=kv_object.lng, lat = kv_object.lat, name = city.name, county = city.county, parish = city.parish,  room_nr=room_nr) 
            except Exception as e:
                logger.error(e)
                cnt+=1
                logger.error(f"Trying {cnt} time")
                time.sleep(cnt)
        raise Exception("Connection error, download failed 15 times")
    def fetch_city_objects(self,city, room_nr,deal_type=1):
        start_time = time.time()
        url=self.format_object_url(deal_type=deal_type,county = city.county,parish=city.parish,rooms= room_nr)
        logger.info(url)
        kv_json_response = requests.get(url).json()
        logger.debug(kv_json_response)
        kv_objects: List[KvObject]=scraper_utils.handle_search_results( kv_json_response, city )
        kv_object_details:List[KvObjectDetails]=list(map(lambda kv_object: self.get_object_details(kv_object=kv_object,city=city,room_nr = room_nr),kv_objects))
        logger.info("Download time --- %s seconds ---" % (time.time() - start_time))
        return (kv_objects,kv_object_details)


rakvere=City(name="Rakvere",county=7,parish=1050)
tallinn=City(name="Tallinn",county=1,parish=1061)
tartu=City(name="Tartu",county=12,parish=1063)
deals= {"1":"sale","2":"rent"}
cities_k={"rakvere":rakvere,"tartu":tartu,"tallinn":tallinn}
    

def scrape_main(city_name="rakvere",deal_type="1",room_nr="1")->None:
    kv = KVBuilder()
    # TODO: to ssm 
    today=date.today().strftime("%Y-%m-%d")
    city = cities_k[city_name]  
    obj = [ ]
    det = [ ]
    logger.info(f"Fetching city named {city.name} with deal type {deal_type} and room_size {room_nr}")
    obj,det = kv.fetch_city_objects( city, deal_type=deal_type, room_nr = room_nr)
    logger.info("Object results are downloaded")  
    if WRITE_TO_S3:
        bucketname=f"{env}-kinnisvara-etl-raw-data-daily-incremental"
        objects_key=f"objects/{deals[deal_type]}/{city.name}/{today}/{room_nr}/kv_objects.json"
        object_details_key=f"details/{deals[deal_type]}/{city.name}/{today}/{room_nr}/kv_objects_details.json"
        s3_utils.s3_put_rows(list(map(lambda kv_obj: json.dumps(kv_obj.__dict__),obj)),bucketname,objects_key)
        #s3_utils.s3_put_dict(list(map(lambda kv_obj: kv_obj.__dict__,obj)),bucketname,object_details_key)
        logger.info(f"Stored {len(obj)}  objects to S3 s3://{bucketname}/{objects_key}")
        #s3_utils.s3_put_dict(list(map(lambda kv_obj_det: kv_obj_det.__dict__,det)),bucketname,object_details_key)
        s3_utils.s3_put_rows(list(map(lambda kv_obj_det: json.dumps(kv_obj_det.__dict__),det)),bucketname,object_details_key)
        logger.info(f"Stored {len(det)} object details to S3 s3://{bucketname}/{object_details_key}")

def lambda_handler(event, context):
    city_name=event["city_name"]
    deal_type=event["deal_type"]
    room_nr=event["room_nr"]
    scrape_main(city_name,deal_type,room_nr)
    return {"status":200, "message":"the scraping was successful"}

def main():
    cities= ["tallinn"]
    rooms=["1"]

    for c in cities:
        for r in rooms:
            scrape_main(city_name=c,deal_type="2",room_nr=r)

if __name__ == "__main__":
    main()

