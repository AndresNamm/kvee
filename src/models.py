class KvObjectDetails:
    def __init__(self,id,lng,lat,name,county,parish,abs_price,abs_size,title,room_nr):
        self.id=id
        self.lng=lng
        self.lat=lat
        self.name=name
        self.county=county
        self.parish=parish
        self.abs_price=abs_price
        self.abs_size=abs_size
        self.title=title
        self.room_nr=room_nr
        self.url="https://www.kv.ee/"+self.id


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