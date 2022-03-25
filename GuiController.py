import PySimpleGUI as sg

import GlobalVariables
from Apis.GodsUnchained.Images import fetchCardImageForProto
from CommonHelpers import qualityFromNumber
from Configs.Gui_Configs import cardImgSize
from Apis.ImmutableX.OrdersApi import loadOrdersForCard
from ImxTransactions.Purchase import buyOrder
from Configs.GlobalConfigs import defaultChooseCardText
from Model.GodsUnchained.Card import Card, Quality


# Helpers
def getSelectedCard():
    if GlobalVariables.selectedAsset is None: return
    return Card(GlobalVariables.selectedAsset, qualityFromNumber(GlobalVariables.selectedQuality))


# Search Button
def handleSearch(searchStr):
    GlobalVariables.searchMatches = fetchMatchingProtos(searchStr, GlobalVariables.protoCache.getAllProtos())
    numResults = len(GlobalVariables.searchMatches)
    for i in range(1, 7):  # number of matches shown on one page
        if i <= numResults:
            img = fetchCardImageForProto(GlobalVariables.searchMatches[i - 1])
            GlobalVariables.window[f"-CARD IMAGE {i}-"].update(img, size=cardImgSize)
        else:
            GlobalVariables.window[f"-CARD IMAGE {i}-"].update()


def fetchMatchingProtos(cardName, protos):
    return list(filter(lambda p: cardName.lower() in p.name.lower(), protos))


# Image Selection
def handleSelectedImg():
    if GlobalVariables.selectedQuality != 0:
        cards = [Card(GlobalVariables.selectedAsset, qualityFromNumber(GlobalVariables.selectedQuality))]
    else:
        # Future support for not specifying a single quality
        cards = [Card(GlobalVariables.selectedAsset, q) for q in Quality]

    fetchAndPresentPrices(cards[0])


# Matching Orders Table
def tableFromMatchingOrders():
    tableFields = ["pxRaw", "currency", "pxUSD"]
    return [["{:.5f}".format(getattr(o, f)) if str(getattr(o, f)).isnumeric() else getattr(o, f) for f in tableFields]
            for o in GlobalVariables.matchingOrders]


def fetchAndPresentPrices(card):
    GlobalVariables.matchingOrders = sorted(loadOrdersForCard(card), key=lambda o: o.pxUSD)
    GlobalVariables.window["-TABLE-"].update(tableFromMatchingOrders())


def resetMatchingOrdersTable():
    GlobalVariables.window["-TABLE-"].update([[]])
    GlobalVariables.window["Choose Card Text"].update(defaultChooseCardText)


def clearTableSelection():
    GlobalVariables.window["-TABLE-"].update(select_rows=[])


# Quality Selection
def handleRadioButtonChange():
    selectedCard = getSelectedCard()
    fetchAndPresentPrices(selectedCard)


# Purchase Button
def handlePurchaseButton():
    res = sg.popup(f"Are you sure you want to purchase {GlobalVariables.selectedOrder.name} "
                   f"for {GlobalVariables.selectedOrder.pxRaw} ({GlobalVariables.selectedOrder.currency})?",
                   title="Confirm Purchase",
                   button_type=sg.POPUP_BUTTONS_YES_NO)

    if res == "Yes":
        clearTableSelection()
        tradeStatus = purchaseSelectedOrder()

        if tradeStatus['status'] == 'success':
            sg.popup(f"Successfully purchased {GlobalVariables.selectedOrder.name} "
                     f"for {GlobalVariables.selectedOrder.pxRaw} {GlobalVariables.selectedOrder.currency}!",
                     title="Purchase Success!")

        else:
            sg.popup(f"Failed to purchase {GlobalVariables.selectedOrder.name}: "
                     f"{tradeStatus['result']}",
                     title="Purchase Failed!")


def purchaseSelectedOrder():
    res = buyOrder(GlobalVariables.selectedOrder)
    return res
