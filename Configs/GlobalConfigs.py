from Model.ImmutableX.Currencies import Currency

godsUnchainedCollectionAddress = "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
imxOrdersApi = "https://api.x.immutable.com/v1/orders?"

imxTokenAddress = "0xf57e7e7c23978c3caec3c3548e3d615c346e79ff"
godsTokenAddress = "0xccc8cb5229b0ac8069c51fd58367fd1e622afd97"
usdcTokenAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

tokenAddressMap = {
    Currency.IMX: imxTokenAddress,
    Currency.GODS: godsTokenAddress,
    Currency.USDC: usdcTokenAddress
}

defaultChooseCardText = "Choose an asset on the left..."
