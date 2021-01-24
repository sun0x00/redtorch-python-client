import logging as logger

from google.protobuf.json_format import MessageToJson

from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService
from xyz.redtorch.client.strategy.StrategyEngine import StrategyEngine


class RpcClientRtnHandler:
    @staticmethod
    def onRpcOrderRtn(rpcOrderRtn):
        ClientTradeCacheService.storeOrder(rpcOrderRtn.order)
        StrategyEngine.onOrder(rpcOrderRtn.order)

    @staticmethod
    def onRpcTradeRtn(rpcTradeRtn):
        ClientTradeCacheService.storeTrade(rpcTradeRtn.trade)
        StrategyEngine.onTrade(rpcTradeRtn.trade)

    @staticmethod
    def onRpcPositionRtn(rpcPositionRtn):
        ClientTradeCacheService.storePosition(rpcPositionRtn.position)

    @staticmethod
    def onRpcAccountRtn(rpcAccountRtn):
        ClientTradeCacheService.storeAccount(rpcAccountRtn.account)

    @staticmethod
    def onRpcContractRtn(rpcContractRtn):
        ClientTradeCacheService.storeContract(rpcContractRtn.contract)

    @staticmethod
    def onRpcTickRtn(rpcTickRtn):
        ClientTradeCacheService.storeTick(rpcTickRtn.tick)
        StrategyEngine.onTick(rpcTickRtn.tick)

    @staticmethod
    def onRpcNoticeRtn(rpcNoticeRtn):
        logger.info("收到通知信息%s" % str(MessageToJson(rpcNoticeRtn)))

    @staticmethod
    def onRpcOrderListRtn(rpcOrderListRtn):
        ClientTradeCacheService.storeOrderList(rpcOrderListRtn.order)
        for order in rpcOrderListRtn.order:
            StrategyEngine.onOrder(order)

    @staticmethod
    def onRpcTradeListRtn(rpcTradeListRtn):
        ClientTradeCacheService.storeTradeList(rpcTradeListRtn.trade)
        for trade in rpcTradeListRtn.trade:
            StrategyEngine.onTrade(trade)

    @staticmethod
    def onRpcContractListRtn(rpcContractListRtn):
        ClientTradeCacheService.storeContractList(rpcContractListRtn.contract)

    @staticmethod
    def onRpcPositionListRtn(rpcPositionListRtn):
        ClientTradeCacheService.storePositionList(rpcPositionListRtn.position)

    @staticmethod
    def onRpcAccountListRtn(rpcAccountListRtn):
        ClientTradeCacheService.storeAccountList(rpcAccountListRtn.account)

    @staticmethod
    def onRpcTickListRtn(rpcTickListRtn):
        ClientTradeCacheService.storeTickList(rpcTickListRtn.tick)
