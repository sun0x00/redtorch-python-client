class ClientTradeCacheService:
    orderDict = dict()
    tradeDict = dict()
    positionDict = dict()
    mixContractDict = dict()
    accountDict = dict()
    mixTickDict = dict()

    @staticmethod
    def storeOrder(order):
        ClientTradeCacheService.orderDict[order.orderId] = order

    @staticmethod
    def storeTrade(trade):
        ClientTradeCacheService.tradeDict[trade.tradeId] = trade

    @staticmethod
    def storeContract(contract):
        ClientTradeCacheService.mixContractDict[contract.unifiedSymbol] = contract

    @staticmethod
    def storePosition(position):
        ClientTradeCacheService.positionDict[position.positionId] = position

    @staticmethod
    def storeAccount(account):
        ClientTradeCacheService.accountDict[account.accountId] = account

    @staticmethod
    def storeTick(tick):
        ClientTradeCacheService.mixTickDict[tick.unifiedSymbol] = tick
