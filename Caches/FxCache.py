from BeautifulSoup.BeautifulSoupHelpers import fetchClassValue
from Model.ImmutableX.Currencies import Currency


class FxVsUSDCache:
    def __init__(self):
        currencies = [Currency.ETH, Currency.USDC, Currency.GODS, Currency.IMX]
        allData = {}
        for c in currencies:
            px = getCryptoPrice(c)
            allData.update({c: float(px)})

        self.data = allData

    def addEntry(self, fx, rate):
        self.data.update({fx: rate})

    def get(self, fx):
        if fx in self.data.keys():
            return self.data.get(fx)
        else:
            px = getCryptoPrice(fx)
            self.addEntry(fx, px)
            return px

    def contains(self, fx):
        return fx in self.data.keys()

    def convertCurrency(self, rawPx, baseFx, targetFx):
        if baseFx == targetFx:
            return rawPx

        baseFxUSDRate = self.get(baseFx)
        targetFxUSDRate = self.get(targetFx)
        return rawPx * baseFxUSDRate / targetFxUSDRate


def loadFxCache(cache):
    currencies = [Currency.ETH, Currency.USDC, Currency.GODS, Currency.IMX]
    for c in currencies:
        px = getCryptoPrice(c)
        cache.addEntry(c, float(px))


def getCryptoPrice(crypto):
    cryptoName = crypto.value
    url = f"https://coinmarketcap.com/currencies/{cryptoName}/"
    c = "priceValue"
    rawPrice = fetchClassValue(url, c)
    cleaned = rawPrice.replace(",", "")[1:]

    return float(cleaned)
