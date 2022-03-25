from Apis.GodsUnchained.FetchGUCards import fetchGUProtos
from Apis.GodsUnchained.Images import loadDefaultImage
from Caches.FxCache import FxVsUSDCache
from Caches.ProtoCache import GodsUnchainedProtoCache

protos = fetchGUProtos()
protoCache = GodsUnchainedProtoCache(protos)
fxCache = FxVsUSDCache()

window = None
searchMatches = []
selectedAsset = None
selectedQuality = 4
matchingOrders = []
selectedOrder = None

defaultImg = loadDefaultImage()

