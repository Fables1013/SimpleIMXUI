from time import sleep

from Configs import GlobalConfigs
import requests
import pytz
from urllib.parse import urlencode, quote_plus

from Model.ImmutableX.Currencies import Currency


def extractJsonFromDict(dict):
    res = []
    for k, v in dict.items():
        res.append(f'"{k}": ["{v}"]')

    return ','.join(r for r in res)


def buildApiMetadata(params):
    if params:
        return '{' + extractJsonFromDict(params) + '}'
    else:
        return ""


def configureApiEndpoint(user=None, sinceDate=None, status=None, card=None, cardName=None, pageSize=200,
                         orderBy="updated_at", salesOrBuys="sell", maxDate=None, direction="desc", quality=None,
                         currency=None, collection=None, proto=None):
    metaDataParams = {}
    params = {}
    if cardName is not None:
        params.update({salesOrBuys + "_token_name": cardName})
    if status is not None:
        params.update({'status': status})
    if sinceDate is not None:
        formattedSinceDate = sinceDate.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        params.update({'updated_min_timestamp': formattedSinceDate})
    if maxDate is not None:
        formattedMaxDate = maxDate.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        params.update({'updated_max_timestamp': formattedMaxDate})
    if user is not None:
        params.update({'user': user})
    if collection is not None:
        if salesOrBuys == "sell":
            params.update({'sell_token_address': GlobalConfigs.godsUnchainedCollectionAddress})
        else:
            params.update({'buy_token_address': GlobalConfigs.godsUnchainedCollectionAddress})
    if quality is not None:
        metaDataParams.update({"quality": quality.value})
    if card is not None:
        metaDataParams.update({"proto": str(card.proto.id)})
        if quality is None:
            metaDataParams.update({"quality": card.quality.value})
    if proto is not None:
        metaDataParams.update({"proto": str(proto.id)})
    if currency is not None:
        sellOrBuyInverted = 'sell' if salesOrBuys == 'buy' else 'buy'
        if currency != Currency.ETH:
            params.update({sellOrBuyInverted + "_token_address": GlobalConfigs.tokenAddressMap[currency]})
        else:
            params.update({sellOrBuyInverted + "_token_type": 'ETH'})

    if metaDataParams:
        params.update({salesOrBuys + '_metadata': buildApiMetadata(metaDataParams)})

    params.update({"order_by": orderBy, "direction": direction, "page_size": str(pageSize)})

    apiEndpoint = GlobalConfigs.imxOrdersApi + urlencode(params, quote_via=quote_plus)

    return apiEndpoint


def collectResultsFromEndpoint(apiEndpoint, maxIterations=100, rateLimit=None):
    maxLoops = maxIterations
    currLoop = 1
    allResults = []
    cursor = ""

    while True:
        try:
            urlWithCursor = apiEndpoint + ";cursor=" + cursor
            res = fetchResult(urlWithCursor)
            if rateLimit is not None:
                sleep(rateLimit)

            if res is None:
                return []
            json = res.json()
            if not json:
                return []
            results = json["result"]

            if results is None:
                break

            if len(results) == 0:
                break
            cursor = json["cursor"]
            allResults = allResults + results

            currLoop += 1
            if currLoop > maxLoops:
                break

            if currLoop % 100 == 0:
                print(str(currLoop))

        except:
            return allResults

    return allResults


def fetchResult(url):
    try:
        return requests.get(url)
    except Exception as e:
        print(str(e))
        return None
