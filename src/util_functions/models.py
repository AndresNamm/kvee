
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
    abs_size:str=""
    abs_price:str=""
    kitchen:str=""
    heating:str=""
    sanruum:str=""
    lisainfo:str=""
    side_ja_turvalisus:str=""
    area:str=""


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