from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService
from xyz.redtorch.client.strategy.StrategyEngine import StrategyEngine
import logging as logger


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
        logger.error("收到通知信息%s", rpcNoticeRtn.notice)

    @staticmethod
    def onRpcOrderListRtn(rpcOrderListRtn):
        for order in rpcOrderListRtn.order:
            ClientTradeCacheService.storeOrder(order)
            StrategyEngine.onOrder(order)

    @staticmethod
    def onRpcTradeListRtn(rpcTradeListRtn):
        for trade in rpcTradeListRtn.trade:
            ClientTradeCacheService.storeTrade(trade)
            StrategyEngine.onTrade(trade)

    @staticmethod
    def onRpcContractListRtn(rpcContractListRtn):
        for contract in rpcContractListRtn.contract:
            ClientTradeCacheService.storeContract(contract)

    @staticmethod
    def onRpcPositionListRtn(rpcPositionListRtn):
        for position in rpcPositionListRtn.position:
            ClientTradeCacheService.storePosition(position)

    @staticmethod
    def onRpcAccountListRtn(rpcAccountListRtn):
        for account in rpcAccountListRtn.account:
            ClientTradeCacheService.storeAccount(account)

    @staticmethod
    def onRpcTickListRtn(rpcTickListRtn):
        for tick in rpcTickListRtn.tick:
            ClientTradeCacheService.storeTick(tick)


