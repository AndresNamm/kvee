
from dataclasses import dataclass,asdict



@dataclass
class KvObjectDetails:
    id: str
    lng: str
    lat: str
    name: str
    county: str
    parish: str
    room_nr: str
    title: str=""
    absolute_size:str=""
    absolute_price:str=""
    kitchen:str=""
    heating:str=""
    sanruum:str=""
    lisainfo:str=""
    side_ja_turvalisus:str=""
    area:str=""
    url: str = 'https://www.kv.ee/'+ str(id)

@dataclass
class KvObject:
    id:str
    lng:str
    lat:str
    name:str
    county:str
    parish:str
@dataclass
class City: 
    name:str
    county:str
    parish:str