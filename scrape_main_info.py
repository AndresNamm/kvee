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
    return (table , lst)


def read_in_objects():
    return [3237939,3230755,3230756]

def add_scraped_objects(lst):
    for l in lst:
        print(l[0])

def main():
    res=[]
    for obj in read_in_objects():
        inf=get_object_details_info(obj)
        res.append(inf)
    add_scraped_objects(res)

main()









