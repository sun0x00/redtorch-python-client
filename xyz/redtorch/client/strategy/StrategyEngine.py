from gevent.lock import RLock


class StrategyEngine:

    __strategyDict = {}
    __strategyDictLock = RLock()
    __engineSwitch = False

    @staticmethod
    def getStrategyByStrategyId(strategyId):
        StrategyEngine.__strategyDictLock.acquire()
        try:
            if strategyId in StrategyEngine.__strategyDict:
                return StrategyEngine.__strategyDict[strategyId]
            else:
                return None
        finally:
            StrategyEngine.__strategyDictLock.release()

    @staticmethod
    def addStrategy(strategy):
        StrategyEngine.__strategyDictLock.acquire()
        try:
            StrategyEngine.__strategyDict[strategy.strategyId] = strategy
        finally:
            StrategyEngine.__strategyDictLock.release()

    @staticmethod
    def removeStrategy(strategyId):
        StrategyEngine.__strategyDictLock.acquire()
        try:
            if strategyId in StrategyEngine.__strategyDict:
                strategy = StrategyEngine.__strategyDict.pop(strategyId)
                return strategy.stopTrading(True)
            return None
        finally:
            StrategyEngine.__strategyDictLock.release()

    @staticmethod
    def onTick(tick):
        StrategyEngine.__strategyDictLock.acquire()
        try:
            msg = {
                    'type': 'tick',
                    'value': tick
                }

            for key in StrategyEngine.__strategyDict.keys():
                strategy = StrategyEngine.__strategyDict[key]
                strategy.putMsg(msg)
        finally:
            StrategyEngine.__strategyDictLock.release()

    @staticmethod
    def onOrder(order):
        StrategyEngine.__strategyDictLock.acquire()
        try:
            msg = {
                    'type': 'order',
                    'value': order
                }

            for key in StrategyEngine.__strategyDict.keys():
                strategy = StrategyEngine.__strategyDict[key]
                strategy.putMsg(msg)
        finally:
            StrategyEngine.__strategyDictLock.release()

    @staticmethod
    def onTrade(trade):
        StrategyEngine.__strategyDictLock.acquire()
        try:
            msg = {
                    'type': 'trade',
                    'value': trade
                }

            for key in StrategyEngine.__strategyDict.keys():
                strategy = StrategyEngine.__strategyDict[key]
                strategy.putMsg(msg)
        finally:
            StrategyEngine.__strategyDictLock.release()

