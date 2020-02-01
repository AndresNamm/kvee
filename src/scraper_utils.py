import numpy as np
import collections
import csv
import logging
import os
from src.models import KvObject
from requests_html import HTMLSession
LOGLEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()



def parse_details_from_html(request_response):
    r=request_response
    parsed_dic={}

    try:
        absolute_size = r.html.find( 'p.object-meta',first = True )  # '<p class="object-meta">2 tuba<span class="sep">|</span>35 m²</p>'
        absolute_size=absolute_size.text.split( '|' )[-1]
        if (absolute_size!=""):
            parsed_dic[ 'absolute_size' ] = int(absolute_size.split( '\xa0' )[0])
        else:
            parsed_dic[ 'absolute_size' ]=0
    except Exception as e:
        logging.error("Issue with parsing the absolute sizes")
        logging.error(r.text)
        logging.error(e)
        parsed_dic[ 'absolute_size' ]=0


    absolute_price = r.html.find( 'p.object-price strong', first = True )  # '<strong>31 000 €</strong>'

    parsed_dic['absolute_price'] = int( ''.join( absolute_price.text.split( '\xa0' )[ :-1 ] ) )
    parsed_dic['title'] = r.html.find( 'p.object-important-note',first = True ).text  # <p class="object-important-note">MÜÜA  KORRALIK 2 TOALINE KORTER KESKLINNAS</p>

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
        for marker in kv_json_response :

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






