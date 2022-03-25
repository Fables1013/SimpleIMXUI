import datetime as dt

from Model.GodsUnchained.Card import Quality


def format(n, f):
    if f == "n":
        return "{:8.6f}".format(n)
    elif f == "p":
        return "{:4.2f}".format(n * 100)
    elif f == "u":
        return "{:6.2f}".format(n)
    else:
        return n


def convertTimestampToDateTime(ts):
    cleanedTs = ts.replace("(", "").replace(")", "")

    try:
        return dt.datetime.strptime(cleanedTs, '%Y-%m-%dT%H:%M:%S.%fZ')
    except Exception:
        return dt.datetime.strptime(cleanedTs, '%Y-%m-%dT%H:%M:%SZ')


def qualityFromNumber(n):
    return {4: Quality.Meteorite, 3: Quality.Shadow, 2: Quality.Gold, 1: Quality.Diamond}[n]


def numberFromQuality(q):
    return {Quality.Meteorite: 4, Quality.Shadow: 3, Quality.Gold: 2, Quality.Diamond: 1}[q]
