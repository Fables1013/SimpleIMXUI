import requests

from Model.GodsUnchained.Proto import Proto


def fetchGUProtos():
    godsAPI = "https://api.godsunchained.com/v0/proto?perPage=4000"
    res = requests.get(godsAPI)
    jsonDict = res.json()
    protos = list(filter(lambda p: p.collectable, map(lambda r: Proto().setFields(r),  jsonDict["records"])))

    return protos
