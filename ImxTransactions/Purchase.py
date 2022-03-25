import Configs.UserConfigs
from ImxTransactions.BuildImxCurrency import buildPurchaseToken
from Model.ImmutableX.Currencies import Currency
from imxpy import CreateTradeParams, ERC721, imx_client


def buyOrder(o):
    if o.currency != Currency.ETH and o.currency != Currency.GODS:
        return

    purchaseCurrency = buildPurchaseToken(o)

    client = imx_client.IMXClient('main', pk=Configs.UserConfigs.privateKey)
    tradeParams = CreateTradeParams(
        order_id=o.orderId,
        sender=Configs.UserConfigs.publicKey,
        token_buy=ERC721(token_id=o.tokenId, contract_addr=o.assetCollection),
        token_sell=purchaseCurrency
    )

    res = client.create_trade(tradeParams)
    return res.result()
