import logging as logger
import uuid
import time

from google.protobuf.json_format import MessageToJson

from xyz.redtorch.client.strategy.StrategyEngine import StrategyEngine

try:
    import thread
except ImportError:
    import _thread as thread

from queue import Queue

from xyz.redtorch.pb.core_field_pb2 import SubmitOrderReqField
from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService
from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService
from xyz.redtorch.pb.core_enum_pb2 import TimeConditionEnum, VolumeConditionEnum, ContingentConditionEnum, \
    HedgeFlagEnum, ForceCloseReasonEnum


class StrategyTemplate:
    def __init__(self, strategySetting):
        self.initSwitch = False
        self.tradingSwitch = False
        if 'strategyId' not in strategySetting:
            raise Exception("策略ID不可为空")
        self.strategySetting = strategySetting
        self.strategyId = strategySetting['strategyId']
        self.subscribedUnifiedSymbolSet = set()
        self.originOrderIdSet = set()
        self.msgQueue = Queue()

    def putMsg(self, msg):
        self.msgQueue.put(msg)

    def processMessage(self):
        strategy = StrategyEngine.getStrategyByStrategyId(self.strategyId)
        while strategy is not None and self is strategy:

            if self.msgQueue.empty():
                time.sleep(0.01)
                strategy = StrategyEngine.getStrategyByStrategyId(self.strategyId)
                continue
            message = self.msgQueue.get()

            if message['type'] == 'tick':
                tick = message['value']
                if tick.unifiedSymbol in self.subscribedUnifiedSymbolSet:
                    self.processTick(tick)
            elif message['type'] == 'trade':
                trade = message['value']
                self.processTrade(trade)
            elif message['type'] == 'order':
                order = message['value']
                self.processOrder(order)

            strategy = StrategyEngine.getStrategyByStrategyId(self.strategyId)

    def initStrategy(self):
        if not self.initSwitch:
            logger.info("尝试初始化策略%s", self.strategyId)
            try:
                self.onInit()
                self.initSwitch = True
                thread.start_new_thread(self.processMessage, ())
            except:
                logger.error("策略%s初始化异常", self.strategyId, exc_info=True)
        else:
            logger.warning("策略%s已经初始化,请勿重复初始化", self.strategyId)

    def startTrading(self):
        if not self.initSwitch:
            logger.error("策略%s尚未初始化,请首先初始化", self.strategyId)
            return

        if not self.tradingSwitch:
            logger.info("尝试启动策略%s", self.strategyId)
            try:
                self.onStartTrading()
                self.tradingSwitch = True
            except:
                logger.error("策略%s启动异常", self.strategyId, exc_info=True)
        else:
            logger.warning("策略%s已经处于交易状态", self.strategyId)

    def stopTrading(self, finishedCorrectly=True):
        if self.tradingSwitch:
            logger.info("尝试停止策略%s", self.strategyId)
            self.tradingSwitch = False
            try:
                self.onStopTrading(finishedCorrectly)
            except:
                logger.error("策略%s停止异常", self.strategyId, exc_info=True)

        else:
            logger.warning("策略%s已经处于停止状态", self.strategyId)

    def processTick(self, tick):
        if self.initSwitch and self.tradingSwitch:
            try:
                self.onTick(tick)
            except:
                self.stopTrading(finishedCorrectly=False)
                logger.error("策略%s处理Tick异常", self.strategyId, exc_info=True)
        else:
            logger.error("拒绝处理Tick,策略%s尚未初始化或未处于交易状态", self.strategyId)

    def processTrade(self, trade):
        if self.initSwitch and self.tradingSwitch:
            try:
                self.onTrade(trade)
            except:
                self.stopTrading(finishedCorrectly=False)
                logger.error("策略%s处理Trade异常", self.strategyId, exc_info=True)
        else:
            logger.error("拒绝处理Trade,策略%s尚未初始化或未处于交易状态", self.strategyId)

    def processOrder(self, order):
        if self.initSwitch and self.tradingSwitch:
            try:
                self.onOrder(order)
            except:
                self.stopTrading(finishedCorrectly=False)
                logger.error("策略%s处理Order异常", self.strategyId, exc_info=True)

        else:
            logger.error("拒绝处理Order,策略%s尚未初始化或未处于交易状态", self.strategyId)

    def onInit(self):
        logger.info("策略%s初始化", self.strategyId)

    def onStartTrading(self):
        logger.info("策略%s开始交易", self.strategyId)

    def onStopTrading(self, finishedCorrectly=True):
        logger.info("策略%s停止交易, %s", self.strategyId, finishedCorrectly)

    def onTick(self, tick):
        # 已经根据订阅过滤了不属于此策略的行情
        print(MessageToJson(tick))

    def onTrade(self, trade):
        # 校验是否是策略发出的定单
        if trade.originOrderId in self.originOrderIdSet:
            print(MessageToJson(trade))

    def onOrder(self, order):
        # 校验是否是策略发出的定单
        if order.originOrderId in self.originOrderIdSet:
            print(MessageToJson(order))

    def submitOrder(self, unifiedSymbol, orderPriceType, direction, offsetFlag, accountId, price, volume,
                    originOrderId=None, sync=True):
        if self.initSwitch and self.tradingSwitch:
            submitOrderReq = SubmitOrderReqField()

            submitOrderReq.contract.CopyFrom(ClientTradeCacheService.getContractByUnifiedSymbol(unifiedSymbol))
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

            account = ClientTradeCacheService.getAccountByAccountId(accountId)

            submitOrderReq.gatewayId = account.gatewayId
            submitOrderReq.accountCode = account.code
            submitOrderReq.currency = account.currency

            if originOrderId is None:
                submitOrderReq.originOrderId = str(uuid.uuid4())
            else:
                submitOrderReq.originOrderId = originOrderId

            self.originOrderIdSet.add(submitOrderReq.originOrderId)

            logger.info("策略%s提交定单 %s", MessageToJson(submitOrderReq), self.strategyId)
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

        logger.info("策略%s订阅合约%s", self.strategyId, unifiedSymbol)
        contract = ClientTradeCacheService.getContractByUnifiedSymbol(unifiedSymbol)
        if contract is not None:
            self.subscribedUnifiedSymbolSet.add(unifiedSymbol)

            if gatewayId is not None:
                contract.gatewayId = gatewayId
            else:
                contract.gatewayId = ""
            RpcClientApiService.subscribe(contract, None, sync=True)
        else:
            logger.error("策略%s订阅行情错误,未能找到合约%s", self.strategyId, unifiedSymbol)

    def unsubscribe(self, unifiedSymbol, gatewayId=None):
        logger.info("策略%s取消订阅合约%s", self.strategyId, unifiedSymbol)
        contract = ClientTradeCacheService.getContractByUnifiedSymbol(unifiedSymbol)
        if contract is not None:
            if unifiedSymbol in self.subscribedUnifiedSymbolSet:
                self.subscribedUnifiedSymbolSet.remove(unifiedSymbol)
            RpcClientApiService.unsubscribe(contract, gatewayId,
                                            sync=True)
        else:
            logger.error("策略%s退订行情错误,未能找到合约%s", self.strategyId, unifiedSymbol)
