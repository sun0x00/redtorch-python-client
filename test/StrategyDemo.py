
from xyz.redtorch.client.strategy.StrategyTemplate import StrategyTemplate


class StrategyDemo(StrategyTemplate):

    def __init__(self, strategySetting):
        super().__init__(strategySetting)

    def onInit(self):
        self.subscribe("sc2009@INE@FUTURES")

    def onTick(self, tick):
        print("收到Tick, UnifiedSymbol: %s, GatewayId %s" % (tick.unifiedSymbol, tick.gatewayId))

    def onTrade(self, trade):
        # 判断是否是当前策略发出的委托的成交
        if trade.originOrderId in self.originOrderIdSet:
            print("收到成交信息")

    def onOrder(self, order):
        # 判断是否是当前策略发出的委托
        if order.originOrderId in self.originOrderIdSet:
            print("收到委托信息")
