import PySimpleGUI as sg

import Configs.GlobalConfigs
import GlobalVariables
from Configs.Gui_Configs import windowSize
from GuiController import tableFromMatchingOrders, resetMatchingOrdersTable, handleSelectedImg, \
    handleRadioButtonChange, handleSearch, handlePurchaseButton

'''
This GUI is a simple UI used to enable users to find and purchase Gods Unchained cards w/o needing to pay a marketplace 
fee (network and royalty fees still apply). 

The left side is a simple search box and then will display icons representing any cards which match your search criteria
and then the right side shows listings available for purchase.

'''


def run_application():
    search_column = [
        [
            sg.Text("Card Name"),
            sg.In(size=(25, 1), enable_events=True, key="-CARDNAME-"),
            sg.Button("Search", key="-SEARCHBUTTON-")
        ],
        [
            sg.Image(enable_events=True, key="-CARD IMAGE 1-"),
            sg.Image(enable_events=True, key="-CARD IMAGE 2-")
        ],
        [
            sg.Image(enable_events=True, key="-CARD IMAGE 3-"),
            sg.Image(enable_events=True, key="-CARD IMAGE 4-")
        ],
        [
            sg.Image(enable_events=True, key="-CARD IMAGE 5-"),
            sg.Image(enable_events=True, key="-CARD IMAGE 6-")
        ]
    ]

    card_purchase_column = [
        [sg.Text(Configs.GlobalConfigs.defaultChooseCardText, key="Choose Card Text")],
        [
            sg.Radio('Meteorite', 'Quality', enable_events=True, key='-QualityRadio4-', default=True),
            sg.Radio('Shadow', 'Quality', enable_events=True, key='-QualityRadio3-', default=False),
            sg.Radio('Gold', 'Quality', enable_events=True, key='-QualityRadio2-', default=False),
            sg.Radio('Diamond', 'Quality', enable_events=True, key='-QualityRadio1-', default=False)
        ],
        [sg.Table(values=tableFromMatchingOrders(), headings=['PX', 'Currency', 'PX USD'],
                  auto_size_columns=False,
                  justification='right',
                  num_rows=20,
                  def_col_width=10,
                  col_widths=[15, 15, 15],
                  key='-TABLE-',
                  row_height=10,
                  enable_events=True,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Purchase', key='PURCHASE-BUTTON', disabled=True)]

    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(search_column),
            sg.VSeperator(),
            sg.Column(card_purchase_column)
        ]
    ]

    GlobalVariables.window = sg.Window("Gods Unchained", layout, size=windowSize)

    # Run the Event Loop
    while True:
        event, values = GlobalVariables.window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-SEARCHBUTTON-":
            resetMatchingOrdersTable()
            searchStr = values["-CARDNAME-"]
            handleSearch(searchStr)

        elif "-CARD IMAGE" in event:
            ind = int(event[-2]) - 1
            if ind >= len(GlobalVariables.searchMatches):
                continue
            GlobalVariables.selectedAsset = GlobalVariables.searchMatches[ind]
            GlobalVariables.window["Choose Card Text"].update(GlobalVariables.selectedAsset.name)
            handleSelectedImg()

        elif "Quality" in event:
            qNum = int(event[-2])
            if qNum != GlobalVariables.selectedQuality:
                GlobalVariables.selectedQuality = qNum
                handleRadioButtonChange()

        elif "PURCHASE-BUTTON" == event:
            handlePurchaseButton()
            handleSelectedImg()

        elif "-TABLE-" in event:
            if len(values["-TABLE-"]) != 0:
                GlobalVariables.selectedOrder = GlobalVariables.matchingOrders[values['-TABLE-'][0]]
                GlobalVariables.window["PURCHASE-BUTTON"].update(disabled=False)

    GlobalVariables.window.close()
