import uuid

from xyz.redtorch.client.strategy.StrategyTemplate import StrategyTemplate
from xyz.redtorch.pb.core_enum_pb2 import OrderPriceTypeEnum, DirectionEnum, OffsetFlagEnum


class StrategyDemo(StrategyTemplate):

    def __init__(self, strategyId):
        super().__init__(strategyId)
        self.tickCount = 0
        self.preOrderId = None
        self.preOriginOrderId = None
        self.priceTick = 0.02

    def onInit(self):
        self.subscribe("au2006@SHFE@FUTURES")

    def onTick(self, tick):
        print("收到Tick, UnifiedSymbol: %s, GatewayId %s" % (tick.unifiedSymbol, tick.gatewayId))

        self.tickCount += 1

        if str(self.tickCount)[-1] == "5":
            self.submitOrder("au2006@SHFE@FUTURES", OrderPriceTypeEnum.OPT_LimitPrice, DirectionEnum.D_Buy,
                             OffsetFlagEnum.OF_Open, "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a",
                             tick.askPrice[0] + self.priceTick, 1,
                             sync=False)
            self.submitOrder("au2006@SHFE@FUTURES", OrderPriceTypeEnum.OPT_LimitPrice, DirectionEnum.D_Sell,
                             OffsetFlagEnum.OF_Open, "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a",
                             tick.bidPrice[0] - self.priceTick, 1,
                             sync=False)

    def onTrade(self, trade):
        print("收到成交信息")
        print(trade)

    def onOrder(self, order):
        print("收到委托信息")
        print(order)
