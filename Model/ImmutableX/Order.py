import datetime as dt

import CommonHelpers
import GlobalVariables
from Configs.GlobalConfigs import  imxTokenAddress, godsTokenAddress, usdcTokenAddress
from Model.ImmutableX.Currencies import Currency
from Model.ImmutableX.OrderType import OrderType
from Model.GodsUnchained.Card import Quality, Card


# My representation of the order dictionary returned by the ImmutableX Api
class Order:

    def __init__(self, card, name, pxRaw, currency, pxEth, pxUSD, ts, tsCreated, isSellOrder, isBuyOrder, orderType,
                 isActive, isFilled, orderId, tokenId, user, pxListed, status, assetCollection):
        self.card = card  # Need to pass in the card quality
        self.name = name
        self.pxRaw = pxRaw
        self.pxListed = pxListed
        self.currency = currency
        self.pxEth = pxEth
        self.pxUSD = pxUSD
        self.ts = ts
        self.tsCreated = tsCreated
        self.isSellOrder = isSellOrder
        self.isBuyOrder = isBuyOrder
        self.orderType = orderType
        self.isActive = isActive
        self.isFilled = isFilled
        self.orderId = orderId
        self.tokenId = tokenId
        self.user = user
        self.status = status
        self.assetCollection = assetCollection


def getOrderName(o):
    try:
        return o["buy"]["data"]["properties"]["name"]
    except Exception:
        try:
            return o["sell"]["data"]["properties"]["name"]
        except Exception:
            return ""


def getOrderPrice(o):
    if o["amount_sold"] is None:
        return o["buy"]["data"]["quantity"]
    elif int(o["amount_sold"]) > 10000:
        return o["amount_sold"]
    else:
        return o["buy"]["data"]["quantity"]


def getOrderPriceScalar(o):
    try:
        return o["buy"]["data"]["decimals"]
    except Exception:
        try:
            return o["sell"]["data"]["decimals"]
        except Exception:
            return 1.0


def getOrderQuality(o):
    qualityIdMap = {1: Quality.Diamond, 2: Quality.Gold, 3: Quality.Shadow, 4: Quality.Meteorite}
    number = 4
    try:
        number = int(o["buy"]["data"]["properties"]["image_url"][-1])
    except Exception:
        try:
            number = int(o["sell"]["data"]["properties"]["image_url"][-1])
        except:
            return qualityIdMap[number]

    return qualityIdMap[number]


def getOrderRawPrice(o):
    listedPx = getOrderListedPrice(o)
    scalar = getOrderPriceScalar(o)
    return float(listedPx) * pow(10, -1 * float(scalar))


def getOrderListedPrice(o):
    listedPx = getOrderPrice(o)
    return listedPx


def getOrderFx(o):
    if getIsSellOrder(o):
        return o["buy"]["type"]
    else:
        return o["sell"]["type"]


def getOrderTokenAddress(o):
    if getIsSellOrder(o):
        return o["buy"]["data"]["token_address"]
    else:
        return o["sell"]["data"]["token_address"]


def getOrderCurrency(o):
    fx = getOrderFx(o)
    add = getOrderTokenAddress(o)

    if fx == 'ETH':
        return Currency.ETH
    elif add == imxTokenAddress:
        return Currency.IMX
    elif add == godsTokenAddress:
        return Currency.GODS
    elif add == usdcTokenAddress:
        return Currency.USDC

    return Currency.ETH


def getOrderTimeStamp(o):
    transactionTime = o["updated_timestamp"]
    return CommonHelpers.convertTimestampToDateTime(transactionTime) - dt.timedelta(hours=5)


def getOrderTimeStampCreated(o):
    transactionTime = o["timestamp"]
    return CommonHelpers.convertTimestampToDateTime(transactionTime) - dt.timedelta(hours=5)


def getIsSellOrder(o):
    try:
        return o["sell"]["type"] == "ERC721"
    except:
        return False


def getOrderStatus(o):
    try:
        return o["status"]
    except:
        return "active"


def getOrderId(o):
    return o["order_id"]


def getOrderTokenId(o):
    sellOrder = getIsSellOrder(o)
    if sellOrder:
        return o["sell"]["data"]["token_id"]
    else:
        return o["buy"]["data"]["token_id"]


def getOrderUser(o):
    return o["user"]


def getAssetCollection(o):
    return o["sell"]["data"]["token_address"]


def orderFromApiResult(apiResult):
    proto = GlobalVariables.protoCache.fromName(getOrderName(apiResult))
    card = Card(proto, getOrderQuality(apiResult))
    pxRaw = getOrderRawPrice(apiResult)
    pxListed = getOrderListedPrice(apiResult)
    currency = getOrderCurrency(apiResult)
    pxEth = GlobalVariables.fxCache.convertCurrency(pxRaw, currency, Currency.ETH)
    isSellOrder = getIsSellOrder(apiResult)
    isBuyOrder = not isSellOrder
    assetCollection = getAssetCollection(apiResult)

    return Order(card=card,  # Need to pass in the card quality
                 name=proto.name,
                 pxRaw=pxRaw,
                 currency=currency,
                 pxEth=pxEth,
                 pxUSD=GlobalVariables.fxCache.convertCurrency(pxEth, Currency.ETH, Currency.USDC),
                 ts=getOrderTimeStamp(apiResult),
                 tsCreated=getOrderTimeStampCreated(apiResult),
                 isSellOrder=isSellOrder,
                 isBuyOrder=isBuyOrder,
                 orderType=OrderType.Buy if isBuyOrder else OrderType.Sell,
                 isActive=getOrderStatus(apiResult) == "active",
                 isFilled=getOrderStatus(apiResult) == "filled",
                 orderId=getOrderId(apiResult),
                 tokenId=getOrderTokenId(apiResult),
                 user=getOrderUser(apiResult),
                 pxListed=pxListed,
                 status=getOrderStatus(apiResult),
                 assetCollection=assetCollection)
