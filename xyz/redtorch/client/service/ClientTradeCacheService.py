from threading import RLock


class ClientTradeCacheService:
    __orderDict = dict()
    __orderDictLock = RLock()
    __tradeDict = dict()
    __tradeDictLock = RLock()
    __positionDict = dict()
    __positionDictLock = RLock()
    __ContractDict = dict()
    __ContractDictLock = RLock()
    __accountDict = dict()
    __accountDictLock = RLock()
    __mixTickDict = dict()
    __mixTickDictLock = RLock()

    @staticmethod
    def getOrderDict():
        ClientTradeCacheService.__orderDictLock.acquire()
        try:
            return ClientTradeCacheService.__orderDict.copy()
        finally:
            ClientTradeCacheService.__orderDictLock.release()

    @staticmethod
    def getTradeDict():
        ClientTradeCacheService.__tradeDictLock.acquire()
        try:
            return ClientTradeCacheService.__tradeDict.copy()
        finally:
            ClientTradeCacheService.__tradeDictLock.release()

    @staticmethod
    def getPositionDict():
        ClientTradeCacheService.__positionDictLock.acquire()
        try:
            return ClientTradeCacheService.__positionDict.copy()
        finally:
            ClientTradeCacheService.__positionDictLock.release()

    @staticmethod
    def getContractDict():
        ClientTradeCacheService.__ContractDictLock.acquire()
        try:
            return ClientTradeCacheService.__ContractDict.copy()
        finally:
            ClientTradeCacheService.__ContractDictLock.release()

    @staticmethod
    def getAccountDict():
        ClientTradeCacheService.__accountDictLock.acquire()
        try:
            return ClientTradeCacheService.__accountDict.copy()
        finally:
            ClientTradeCacheService.__accountDictLock.release()

    @staticmethod
    def getMixTickDict():
        ClientTradeCacheService.__mixTickDictLock.acquire()
        try:
            return ClientTradeCacheService.__mixTickDict.copy()
        finally:
            ClientTradeCacheService.__mixTickDictLock.release()

    @staticmethod
    def storeOrder(order):
        ClientTradeCacheService.__orderDictLock.acquire()
        try:
            ClientTradeCacheService.__orderDict[order.orderId] = order
        finally:
            ClientTradeCacheService.__orderDictLock.release()

    @staticmethod
    def storeOrderList(orderList):
        ClientTradeCacheService.__orderDictLock.acquire()
        try:
            for order in orderList:
                ClientTradeCacheService.__orderDict[order.orderId] = order
        finally:
            ClientTradeCacheService.__orderDictLock.release()

    @staticmethod
    def storeTrade(trade):
        ClientTradeCacheService.__tradeDictLock.acquire()
        try:
            ClientTradeCacheService.__tradeDict[trade.tradeId] = trade
        finally:
            ClientTradeCacheService.__tradeDictLock.release()

    @staticmethod
    def storeTradeList(tradeList):
        ClientTradeCacheService.__tradeDictLock.acquire()
        try:
            for trade in tradeList:
                ClientTradeCacheService.__tradeDict[trade.tradeId] = trade
        finally:
            ClientTradeCacheService.__tradeDictLock.release()

    @staticmethod
    def storeContract(contract):
        ClientTradeCacheService.__ContractDictLock.acquire()
        try:
            ClientTradeCacheService.__ContractDict[contract.uniformSymbol] = contract
        finally:
            ClientTradeCacheService.__ContractDictLock.release()


    @staticmethod
    def storeContractList(contractList):
        ClientTradeCacheService.__ContractDictLock.acquire()
        try:
            for contract in contractList:
                ClientTradeCacheService.__ContractDict[contract.uniformSymbol] = contract
        finally:
            ClientTradeCacheService.__ContractDictLock.release()

    @staticmethod
    def storePosition(position):
        ClientTradeCacheService.__positionDictLock.acquire()
        try:
            ClientTradeCacheService.__positionDict[position.positionId] = position
        finally:
            ClientTradeCacheService.__positionDictLock.release()

    @staticmethod
    def storePositionList(positionList):
        ClientTradeCacheService.__positionDictLock.acquire()
        try:
            for position in positionList:
                ClientTradeCacheService.__positionDict[position.positionId] = position
        finally:
            ClientTradeCacheService.__positionDictLock.release()

    @staticmethod
    def storeAccount(account):
        ClientTradeCacheService.__accountDictLock.acquire()
        try:
            ClientTradeCacheService.__accountDict[account.accountId] = account
        finally:
            ClientTradeCacheService.__accountDictLock.release()

    @staticmethod
    def storeAccountList(accountList):
        ClientTradeCacheService.__accountDictLock.acquire()
        try:
            for account in accountList:
                ClientTradeCacheService.__accountDict[account.accountId] = account
        finally:
            ClientTradeCacheService.__accountDictLock.release()

    @staticmethod
    def storeTick(tick):
        ClientTradeCacheService.__mixTickDictLock.acquire()
        try:
            ClientTradeCacheService.__mixTickDict[tick.uniformSymbol] = tick
        finally:
            ClientTradeCacheService.__mixTickDictLock.release()

    @staticmethod
    def storeTickList(tickList):
        ClientTradeCacheService.__mixTickDictLock.acquire()
        try:
            for tick in tickList:
                ClientTradeCacheService.__mixTickDict[tick.uniformSymbol] = tick
        finally:
            ClientTradeCacheService.__mixTickDictLock.release()

    @staticmethod
    def getPositionByPositionKey(positionKey):
        if not positionKey:
            return None
        ClientTradeCacheService.__positionDictLock.acquire()
        try:
            if positionKey in ClientTradeCacheService.__positionDict:
                return ClientTradeCacheService.__positionDict[positionKey]
            return None
        finally:
            ClientTradeCacheService.__positionDictLock.release()

    @staticmethod
    def getTickByUniformSymbol(uniformSymbol):
        if not uniformSymbol:
            return None
        ClientTradeCacheService.__mixTickDictLock.acquire()
        try:
            if uniformSymbol in ClientTradeCacheService.__mixTickDict:
                return ClientTradeCacheService.__mixTickDict[uniformSymbol]
            return None
        finally:
            ClientTradeCacheService.__mixTickDictLock.release()

    @staticmethod
    def getContractByUniformSymbol(uniformSymbol):
        if not uniformSymbol:
            return None
        ClientTradeCacheService.__ContractDictLock.acquire()
        try:
            if uniformSymbol in ClientTradeCacheService.__ContractDict:
                return ClientTradeCacheService.__ContractDict[uniformSymbol]
            return None
        finally:
            ClientTradeCacheService.__ContractDictLock.release()

    @staticmethod
    def getAccountByAccountId(accountId):
        if not accountId:
            return None
        ClientTradeCacheService.__accountDictLock.acquire()
        try:
            if accountId in ClientTradeCacheService.__accountDict:
                return ClientTradeCacheService.__accountDict[accountId]
            return None
        finally:
            ClientTradeCacheService.__accountDictLock.release()
