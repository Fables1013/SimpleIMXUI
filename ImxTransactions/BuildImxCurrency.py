import Configs.GlobalConfigs
from Model.ImmutableX.Currencies import Currency
from imxpy import ERC20, ETH


def buildPurchaseToken(order):
    orderFx = order.currency

    if orderFx == Currency.GODS:
        return ERC20(symbol="$GODS",
                     contract_addr=Configs.GlobalConfigs.tokenAddressMap[Currency.GODS],
                     quantity=order.pxListed,
                     as_wei=True)
    elif orderFx == Currency.ETH:
        return ETH(quantity=order.pxListed, as_wei=True)
    else:
        raise (orderFx.value + " purchases are not supported")
