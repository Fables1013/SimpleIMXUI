import Apis.ImmutableX.ImmutableApiHelpers as IMXHelpers
from Configs.GlobalConfigs import godsUnchainedCollectionAddress
from Model.ImmutableX.Order import orderFromApiResult


def getAllTypedOrdersSinceDate(sinceDate=None, status=None, cardName=None, pageSize=200, user=None, sellOrBuy="sell",
                               maxDate=None, maxIterations=20, quality=None, orderBy='updated_at',
                               currency=None, card=None, proto=None, rateLimit=None, direction='desc', collection=None):

    apiEndpoint = IMXHelpers.configureApiEndpoint(user=user, sinceDate=sinceDate, status=status, cardName=cardName,
                                                  pageSize=pageSize, salesOrBuys=sellOrBuy, maxDate=maxDate,
                                                  orderBy=orderBy, quality=quality, currency=currency, card=card,
                                                  direction=direction, collection=collection, proto=proto)

    allOrders = IMXHelpers.collectResultsFromEndpoint(apiEndpoint, maxIterations, rateLimit)

    orderObjects = list(map(lambda o: orderFromApiResult(o), allOrders))

    return orderObjects


def loadInfoOnProto(proto):
    activeOrders = getAllTypedOrdersSinceDate(status='active', collection=godsUnchainedCollectionAddress, proto=proto,
                                              rateLimit=0.2)

    return activeOrders


def loadOrdersForCard(card):
    activeOrders = getAllTypedOrdersSinceDate(status='active', collection=godsUnchainedCollectionAddress, card=card,
                                              rateLimit=0.2, maxIterations=1)

    return activeOrders
