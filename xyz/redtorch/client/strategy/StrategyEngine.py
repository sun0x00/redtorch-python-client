import logging as logger
import time
from queue import Queue

try:
    import thread
except ImportError:
    import _thread as thread


class StrategyEngine:
    strategyDict = {}

    msgQueue = Queue()

    engineSwitch = False

    @staticmethod
    def start():
        if not StrategyEngine.engineSwitch:
            logger.info("启动异步处理线程")
            thread.start_new_thread(StrategyEngine.processMessage, ())
            StrategyEngine.engineSwitch = True

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
        StrategyEngine.msgQueue.put(
            {
                'type': 'tick',
                'value': tick
            }
        )

    @staticmethod
    def onOrder(order):
        StrategyEngine.msgQueue.put(
            {
                'type': 'order',
                'value': order
            }
        )

    @staticmethod
    def onTrade(trade):
        StrategyEngine.msgQueue.put(
            {
                'type': 'trade',
                'value': trade
            }
        )

    # 采用异步处理避免阻塞问题
    @staticmethod
    def processMessage():
        while True:
            if StrategyEngine.msgQueue.empty():
                time.sleep(0.01)
                continue
            message = StrategyEngine.msgQueue.get()

            if message['type'] == 'tick':
                tick = message['value']
                for key in StrategyEngine.strategyDict.keys():
                    strategy = StrategyEngine.strategyDict[key]
                    if tick.unifiedSymbol in strategy.subscribedUnifiedSymbolSet:
                        strategy.processTick(tick)
            elif message['type'] == 'trade':
                trade = message['value']
                for key in StrategyEngine.strategyDict.keys():
                    strategy = StrategyEngine.strategyDict[key]
                    strategy.processTrade(trade)
            elif message['type'] == 'order':
                order = message['value']
                for key in StrategyEngine.strategyDict.keys():
                    strategy = StrategyEngine.strategyDict[key]
                    strategy.processOrder(order)
