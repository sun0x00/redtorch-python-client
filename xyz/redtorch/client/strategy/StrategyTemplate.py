import logging as logger
import uuid

from xyz.redtorch.pb.core_field_pb2 import SubmitOrderReqField
from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService
from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService
from xyz.redtorch.pb.core_enum_pb2 import TimeConditionEnum,VolumeConditionEnum,ContingentConditionEnum,HedgeFlagEnum,ForceCloseReasonEnum


class StrategyTemplate:
    def __init__(self, strategyId):
        self.initSwitch = False
        self.tradingSwitch = False
        self.strategyId = strategyId
        self.subscribedUnifiedSymbolSet = set()
        self.originOrderIdSet = set()

    def initStrategy(self):
        if not self.initSwitch:
            try:
                self.onInit()
                self.initSwitch = True
            except Exception as e:
                logger.error("策略%s初始化异常", self.strategyId)
                logger.error(e, exc_info=True)
        else:
            logger.warning("策略%s已经初始化,请勿重复初始化", self.strategyId)

    def startTrading(self):
        if not self.initSwitch:
            logger.error("策略%s尚未初始化,请首先初始化", self.strategyId)
            return

        if not self.tradingSwitch:
            try:
                self.onStartTrading()
                self.tradingSwitch = True
            except Exception as e:
                logger.error("策略%s启动异常", self.strategyId)
                logger.error(e, exc_info=True)
        else:
            logger.warning("策略%s已经处于交易状态", self.strategyId)

    def stopTrading(self, finishedCorrectly=True):
        if self.tradingSwitch:
            self.tradingSwitch = False
            try:
                self.onStopTrading(finishedCorrectly)
            except Exception as e:
                logger.error("策略%s停止异常", self.strategyId)
                logger.error(e, exc_info=True)

    def processTick(self, tick):
        if self.initSwitch and self.tradingSwitch:
            try:
                self.onTick(tick)
            except Exception as e:
                self.stopTrading(finishedCorrectly=False)
                logger.error("策略%s处理Tick异常", self.strategyId)
                logger.error(e, exc_info=True)

    def processTrade(self, trade):
        if self.initSwitch and self.tradingSwitch:
            try:
                self.onTrade(trade)
            except Exception as e:
                self.stopTrading(finishedCorrectly=False)
                logger.error("策略%s处理Trade异常", self.strategyId)
                logger.error(e, exc_info=True)

    def processOrder(self, order):
        if self.initSwitch and self.tradingSwitch:
            try:
                self.onOrder(order)
            except Exception as e:
                self.stopTrading(finishedCorrectly=False)
                logger.error("策略%s处理Order异常", self.strategyId)
                logger.error(e, exc_info=True)

    def onInit(self):
        logger.info("策略%s初始化", self.strategyId)

    def onStartTrading(self):
        logger.info("策略%s开始交易", self.strategyId)

    def onStopTrading(self, finishedCorrectly=True):
        logger.info("策略%s停止交易, %s", self.strategyId, finishedCorrectly)

    def onTick(self, tick):
        # 已经根据订阅过滤了不属于此策略的行情
        print(tick)

    def onTrade(self, trade):
        # 校验是否是策略发出的定单
        if trade.originOrderId in self.originOrderIdSet:
            print(trade)

    def onOrder(self, order):
        # 校验是否是策略发出的定单
        if order.originOrderId in self.originOrderIdSet:
            print(order)

    def submitOrder(self, unifiedSymbol, orderPriceType, direction, offsetFlag, accountId, price, volume, originOrderId=None,sync=True):
        if self.initSwitch and self.tradingSwitch:
            submitOrderReq = SubmitOrderReqField()

            submitOrderReq.contract.CopyFrom(ClientTradeCacheService.mixContractDict[unifiedSymbol])
            submitOrderReq.direction = direction
            submitOrderReq.offsetFlag = offsetFlag
            submitOrderReq.orderPriceType = orderPriceType
            submitOrderReq.timeCondition = TimeConditionEnum.TC_GFD
            submitOrderReq.price = price
            submitOrderReq.minVolume = 1
            submitOrderReq.stopPrice = 0.0
            submitOrderReq.volumeCondition = VolumeConditionEnum.VC_AV
            submitOrderReq.contingentCondition = ContingentConditionEnum.CC_Immediately
            submitOrderReq.hedgeFlag = HedgeFlagEnum.HF_Speculation
            submitOrderReq.forceCloseReason = ForceCloseReasonEnum.FCR_NotForceClose
            submitOrderReq.volume = volume

            account = ClientTradeCacheService.accountDict[accountId]

            submitOrderReq.gatewayId = account.gatewayId
            submitOrderReq.accountCode = account.code
            submitOrderReq.currency = account.currency

            if originOrderId is None:
                submitOrderReq.originOrderId = str(uuid.uuid4())
            else:
                submitOrderReq.originOrderId = originOrderId

            self.originOrderIdSet.add(submitOrderReq.originOrderId)

            logger.warning("策略%s提交定单 \n %s", submitOrderReq, self.strategyId)
            if sync:
                orderId = RpcClientApiService.submitOrder(submitOrderReq, sync=True)
                return orderId
            else:
                RpcClientApiService.submitOrder(submitOrderReq, sync=False)
                return None
        else:
            logger.error("策略尚未初始化或未处于交易状态")
            return None

    def cancelOrder(self, orderId=None, originOrderId=None, reqId=None, sync=False):
        RpcClientApiService.cancelOrder(orderId=orderId, originOrderId=originOrderId, reqId=reqId, sync=sync)

    def subscribe(self, unifiedSymbol, gatewayId=None):
        if unifiedSymbol in ClientTradeCacheService.mixContractDict:
            self.subscribedUnifiedSymbolSet.add(unifiedSymbol)
            contract = ClientTradeCacheService.mixContractDict[unifiedSymbol]
            if gatewayId is not None:
                contract.gatewayId = gatewayId
            else:
                contract.gatewayId = ""
            RpcClientApiService.subscribe(ClientTradeCacheService.mixContractDict[unifiedSymbol], None, sync=True)
        else:
            logger.error("策略%s订阅行情错误,未能找到合约%s", self.strategyId, unifiedSymbol)

    def unsubscribe(self, unifiedSymbol, gatewayId=None):
        if unifiedSymbol in ClientTradeCacheService.mixContractDict:
            self.subscribedUnifiedSymbolSet.add(unifiedSymbol)
            RpcClientApiService.unsubscribe(ClientTradeCacheService.mixContractDict[unifiedSymbol], gatewayId,
                                            sync=True)
        else:
            logger.error("策略%s退订行情错误,未能找到合约%s", self.strategyId, unifiedSymbol)
