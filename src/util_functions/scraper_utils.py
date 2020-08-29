import numpy as np
import collections
import csv
import logging
from typing import Final
import os
from util_functions.models import KvObject
from requests_html import HTMLSession

env=os.getenv('ENVIRONMENT','dev')
log_level: Final[str] = os.getenv('LOGLEVEL', 'INFO')

logging.getLogger(__name__).setLevel(log_level)
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

def parse_details_from_html(request_response)->dict:
    r=request_response
    parsed_dic={}
    raw_absolute_size=r.html.find('span.gm-desktop',first=True)
    raw_absolute_price=r.html.find('h3.gm-overlay-price',first=True)
    
    raw_title= r.html.find('p.gm-overlay-header',first=True)
    if raw_title==None:
        raw_title=r.html.find('h2.gm-overlay-title',first=True)
    raw_info=r.html.find('p.gm-overlay-info-1',first=True)
    for line in raw_absolute_size.text.split('\n'):
        if 'Pind:' in line:      
            parsed_dic['abs_size'] = line.split(':')[1].strip().split('\xa0')[0]
    parsed_dic['abs_price'] = int("".join(raw_absolute_price.text.split( '\xa0' )[:-1]))
    parsed_dic['title']=raw_title.text
    # because some items have accented letter we want to remove these for safety 
    replace_map={'köök':'kitchen','küte_ja_ventilatsioon':'heating','sanruum':'sanruum','side_ja_turvalisus':'side_ja_turvalisus','ümbrus':'area','lisainfo':'lisainfo'}
    info={}
    for item in raw_info.text.split('\n'):
        if len(item.split(":"))>1:
            key=item.split(":")[0].replace(' ','_').lower() 
            if key in replace_map:
                key=replace_map[key]
                val=item.split(":")[1]
                info[key]=val
    parsed_dic.update(info)
    return parsed_dic

def handle_search_results( kv_json_response, city) :
    data_objects = [ ]
    if type(kv_json_response) == dict:
        kv_markers = kv_json_response['markers']
        for marker in kv_markers :
            lng = marker[ '1' ]
            lat = marker[ '0' ]
            if 'object_ids' in marker :
                object_ids = marker[ 'object_ids' ].split( '.' )
            elif 'object_id' in marker :
                object_ids = marker[ 'object_id' ].split( '.' )
            else :
                continue
            for obj_id in object_ids:
                result=KvObject(id=obj_id,lng=lng,lat=lat,name=city.name,county=city.county,parish=city.parish)
                data_objects.append(result)
    else :
        for marker in kv_json_response:
            lat = marker[ 0 ]
            lng = marker[ 1 ]
            obj_id = marker[ 2 ]
            result = KvObject( id = obj_id, lng = lng, lat = lat, name = city.name, county = city.county,
                                parish = city.parish )

            data_objects.append( result )

    return data_objects


def retrieve_object_details(object_id):
    address = 'https://kv.ee/?act=search.objectinfo&object_id={}'.format( object_id )
    session = HTMLSession()
    r = session.get(address)
    details = parse_details_from_html( r )
    return details






