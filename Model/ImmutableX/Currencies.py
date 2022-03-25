from enum import Enum
from numpy import format_float_positional
from imxpy import ETH, ERC20


class Currency(Enum):
    ETH = "ethereum"
    USDC = "usd-coin"
    GODS = "gods-unchained"
    IMX = "immutable-x"


def buildCurrency(currency, px):
    if currency == Currency.ETH:
        return ETH(quantity=str(format_float_positional(px, trim='-', precision=18)))
    if currency == Currency.USDC:
        raise Exception(f'Auto listing of {currency} not yet supported')
    if currency == Currency.IMX:
        raise Exception(f'Auto listing of {currency} not yet supported')
    if currency == Currency.GODS:
        raise Exception(f'Auto listing of {currency} not yet supported')
        # return ERC20(quantity=str(format_float_positional(px, trim='-', precision=18)))

