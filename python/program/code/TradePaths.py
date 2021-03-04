"""
NAME: TradePaths.py
AUTHOR: Tanaka Chitete
PURPOSE: Get and print all trade paths between two given assets
CREATION: 04/03/2021
LAST MODIFICATION: 04/03/2021
"""

import TradePathsHelper
import TradePairsAndTradePathsHelper
import UserInterface

"""
NAME: subMenu
IMPORT(S): None
EXPORT(S): None
PURPOSE: Print sub-menu and prepare to launch user-specified operation
CREATION: 04/03/2021
LAST MODIFICATION: 04/03/2021
"""

def subMenu():
    exchangeInfo = None
    while True:
        print("Get and Display All Trade Paths Between Two Crypto-currencies\n\n" + \
            "1. Display\n" + \
            "2. Make Live Request\n" + \
            "3. Load from File\n" + \
            "4. Save to File\n" + \
            "0. Exit\n"
        )
        prompt = "Selection: "
        selection = UserInterface.getInt(0, 4, prompt)

        print() # Formatting purposes

        if selection == 1:
            printTradePaths(exchangeInfo)
        elif selection == 2:
            TradePairsAndTradePathsHelper.getExchangeInfoFromAPI(exchangeInfo)
        elif selection == 3:
            JSON_IOWrapper.loadFromFile(exchangeInfo)
        elif selection == 4:
            JSON_IOWrapper.saveToFile(exchangeInfo)


"""
NAME: printTradePaths
IMPORT(S): exchangeInfo (dict)
EXPORT(S): None
PURPOSE: Using cryptoGraph, print all trade paths between base and quote
CREATION: 04/03/2021
LAST MODIFICATION: 04/03/2021
"""

def printTradePaths(exchangeInfo):
    if exchangeInfo is None:
        print("Cannot display before making live request or loading from file")
    else:
        cryptoGraph = TradePathsHelper.makeCryptoGraph(exchangeInfo)

        prompt = "Start crypto-currency (case-insensitive): "
        start = UserInterface.getStr(prompt)

        prompt = "Destination crypto-currency (case-insensitive): "
        dest = UserInterface.getStr(prompt)

        print() # Formatting purposes

        print("All Trade Paths from {start} to {dest}\n")

        cryptoGraph.printPaths(start, dest)