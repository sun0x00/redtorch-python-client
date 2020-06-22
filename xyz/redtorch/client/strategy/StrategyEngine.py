class StrategyEngine:

    strategyDict = {}
    engineSwitch = False

    @staticmethod
    def addStrategy(strategy):
        StrategyEngine.strategyDict[strategy.strategyId] = strategy

    @staticmethod
    def removeStrategy(strategyId):
        if strategyId in StrategyEngine.strategyDict:
            strategy = StrategyEngine.strategyDict.pop(strategyId)
            return strategy.stopTrading(True)
        return None

    @staticmethod
    def onTick(tick):
        msg = {
                'type': 'tick',
                'value': tick
            }

        for key in StrategyEngine.strategyDict.keys():
            strategy = StrategyEngine.strategyDict[key]
            strategy.putMsg(msg)

    @staticmethod
    def onOrder(order):
        msg = {
                'type': 'order',
                'value': order
            }

        for key in StrategyEngine.strategyDict.keys():
            strategy = StrategyEngine.strategyDict[key]
            strategy.putMsg(msg)

    @staticmethod
    def onTrade(trade):
        msg = {
                'type': 'trade',
                'value': trade
            }

        for key in StrategyEngine.strategyDict.keys():
            strategy = StrategyEngine.strategyDict[key]
            strategy.putMsg(msg)

