import logging as logger

from google.protobuf.json_format import MessageToJson

from xyz.redtorch.client.strategy.StrategyTemplate import StrategyTemplate
from xyz.redtorch.pb.core_enum_pb2 import OrderPriceTypeEnum, DirectionEnum, OffsetFlagEnum


class StrategyDemo(StrategyTemplate):

    def __init__(self, strategySetting):
        super().__init__(strategySetting)
        self.count = 0
        self.long = True
        self.orderId = None

    def onInit(self):
        self.subscribe("cu2103@SHFE@FUTURES")

    def onTick(self, tick):
        self.count += 1
        if self.count % 2 == 0:
            if self.long:
                orderId = self.submitOrder("cu2103@SHFE@FUTURES", OrderPriceTypeEnum.OPT_LimitPrice,
                                           DirectionEnum.D_Buy,
                                           OffsetFlagEnum.OF_Open, "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a",
                                           tick.lastPrice + 10, 1, None, True)
                self.long = False
            else:
                orderId = self.submitOrder("cu2103@SHFE@FUTURES", OrderPriceTypeEnum.OPT_LimitPrice,
                                           DirectionEnum.D_Sell,
                                           OffsetFlagEnum.OF_CloseToday,
                                           "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a", tick.lastPrice - 10, 1,
                                           None, True)
                self.long = True
                # self.cancelOrder(orderId=self.orderId)
        logger.info("收到Tick, UnifiedSymbol: %s, GatewayId %s, 时间戳%s", tick.unifiedSymbol, tick.gatewayId, tick.actionTimestamp)

    def onTrade(self, trade):
        # 校验是否是策略发出的定单
        if trade.originOrderId in self.originOrderIdSet:
            logger.info("策略%s收到Trade:%s", self.strategyId, MessageToJson(trade))

    def onOrder(self, order):
        # 校验是否是策略发出的定单
        if order.originOrderId in self.originOrderIdSet:
            logger.info("策略%s收到Order:%s", self.strategyId, MessageToJson(order))
