class KvObjectDetails:
    def __init__(self,id,lng):
        self.id=id
        self.lng=lng


class KvObject:
    def __init__(self,id,lng,lat,name,county,parish):
        self.id=id
        self.lng=lng
        self.lat=lat
        self.name=name
        self.county=county
        self.parish=parish

class City: 
    def __init__(self,name,county,parish):
        self.name=name
        self.county=county
        self.parish=parish


import json

kv_det=[KvObjectDetails(id=10,lng="assa").__dict__]

print(json.dumps(kv_det))
json.dumps(kv_det)


