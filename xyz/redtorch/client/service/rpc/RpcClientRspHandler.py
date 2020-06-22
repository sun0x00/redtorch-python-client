import logging as logger
from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService


class RpcClientRspHandler:
    waitReqIdSet = set()

    rpcSubscribeRspDict = dict()
    rpcUnsubscribeRspDict = dict()
    rpcSubmitOrderRspDict = dict()
    rpcCancelOrderRspDict = dict()
    rpcSearchContractRspDict = dict()
    rpcExceptionRspDict = dict()

    rpcGetMixContractListRspDict = dict()
    rpcGetPositionListRspDict = dict()
    rpcGetTradeListRspDict = dict()
    rpcGetOrderListRspDict = dict()
    rpcGetTickListRspDict = dict()
    rpcGetAccountListRspDict = dict()

    rpcQueryDBBarListRspDict = dict()

    @staticmethod
    def getAndRemoveRpcSubscribeRsp(reqId):
        if reqId in RpcClientRspHandler.rpcSubscribeRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcSubscribeRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcUnsubscribeRsp(reqId):
        if reqId in RpcClientRspHandler.rpcUnsubscribeRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcUnsubscribeRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcSubmitOrderRsp(reqId):
        if reqId in RpcClientRspHandler.rpcSubmitOrderRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcSubmitOrderRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcCancelOrderRsp(reqId):
        if reqId in RpcClientRspHandler.rpcCancelOrderRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcCancelOrderRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcSearchContractRsp(reqId):
        if reqId in RpcClientRspHandler.rpcSearchContractRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcSearchContractRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcExceptionRsp(reqId):
        if reqId in RpcClientRspHandler.rpcExceptionRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcExceptionRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcGetMixContractListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcGetMixContractListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcGetMixContractListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcGetPositionListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcGetPositionListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcGetPositionListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcGetTradeListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcGetTradeListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcGetTradeListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcGetOrderListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcGetOrderListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcGetOrderListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcGetTickListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcGetTickListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcGetTickListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcQueryDBBarListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcQueryDBBarListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcQueryDBBarListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def getAndRemoveRpcGetAccountListRsp(reqId):
        if reqId in RpcClientRspHandler.rpcGetAccountListRspDict:
            if reqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.waitReqIdSet.remove(reqId)
            return RpcClientRspHandler.rpcGetAccountListRspDict.pop(reqId)
        else:
            return None

    @staticmethod
    def registerWaitReqId(reqId):
        RpcClientRspHandler.waitReqIdSet.add(reqId)

    @staticmethod
    def unregisterWaitReqId(reqId):
        RpcClientRspHandler.waitReqIdSet.remove(reqId)

    @staticmethod
    def onSubscribeRsp(rpcSubscribeRsp):
        reqId = rpcSubscribeRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcSubscribeRspDict[reqId] = rpcSubscribeRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

    @staticmethod
    def onUnsubscribeRsp(rpcUnsubscribeRsp):
        reqId = rpcUnsubscribeRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcUnsubscribeRspDict[reqId] = rpcUnsubscribeRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

    @staticmethod
    def onSubmitOrderRsp(rpcSubmitOrderRsp):
        reqId = rpcSubmitOrderRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcSubmitOrderRspDict[reqId] = rpcSubmitOrderRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

    @staticmethod
    def onCancelOrderRsp(rpcCancelOrderRsp):
        reqId = rpcCancelOrderRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcCancelOrderRspDict[reqId] = rpcCancelOrderRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

    @staticmethod
    def onSearchContractRsp(rpcSearchContractRsp):
        reqId = rpcSearchContractRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcSearchContractRspDict[reqId] = rpcSearchContractRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

    @staticmethod
    def onGetMixContractListRsp(rpcGetMixContractListRsp):
        reqId = rpcGetMixContractListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcGetMixContractListRspDict[reqId] = rpcGetMixContractListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

        if rpcGetMixContractListRsp.contract:
            for tmpContract in rpcGetMixContractListRsp.contract:
                ClientTradeCacheService.storeContract(tmpContract)

    @staticmethod
    def onGetAccountListRsp(rpcGetAccountListRsp):
        reqId = rpcGetAccountListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcGetAccountListRspDict[reqId] = rpcGetAccountListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

        if rpcGetAccountListRsp.account:
            for tmpAccount in rpcGetAccountListRsp.account:
                ClientTradeCacheService.storeAccount(tmpAccount)

    @staticmethod
    def onGetPositionListRsp(rpcGetPositionListRsp):
        reqId = rpcGetPositionListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcGetPositionListRspDict[reqId] = rpcGetPositionListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

        if rpcGetPositionListRsp.position:
            for tmpPosition in rpcGetPositionListRsp.position:
                ClientTradeCacheService.storePosition(tmpPosition)

    @staticmethod
    def onGetTradeListRsp(rpcGetTradeListRsp):
        reqId = rpcGetTradeListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcGetTradeListRspDict[reqId] = rpcGetTradeListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

        if rpcGetTradeListRsp.trade:
            for tmpTrade in rpcGetTradeListRsp.trade:
                ClientTradeCacheService.storeTrade(tmpTrade)

    @staticmethod
    def onGetOrderListRsp(rpcGetOrderListRsp):
        reqId = rpcGetOrderListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcGetOrderListRspDict[reqId] = rpcGetOrderListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

        if rpcGetOrderListRsp.order:
            for tmpOrder in rpcGetOrderListRsp.order:
                ClientTradeCacheService.storeOrder(tmpOrder)

    @staticmethod
    def onGetTickListRsp(rpcGetTickListRsp):
        reqId = rpcGetTickListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcGetTickListRspDict[reqId] = rpcGetTickListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

        if rpcGetTickListRsp.tick:
            for tmpTick in rpcGetTickListRsp.tick:
                ClientTradeCacheService.storeTick(tmpTick)

    @staticmethod
    def onExceptionRsp(rpcExceptionRsp):
        if rpcExceptionRsp.originalReqId:
            logger.error("接收到异常回报,请求ID:%s,异常信息:%s", rpcExceptionRsp.originalReqId, rpcExceptionRsp.info)
            if rpcExceptionRsp.originalReqId in RpcClientRspHandler.waitReqIdSet:
                RpcClientRspHandler.rpcExceptionRspDict[rpcExceptionRsp.originalReqId] = rpcExceptionRsp
        else:
            logger.error("接收到未知请求ID的异常回报,异常信息:%s", rpcExceptionRsp.info)

    @staticmethod
    def onQueryDBBarListRsp(rpcQueryDBBarListRsp):
        reqId = rpcQueryDBBarListRsp.commonRsp.reqId
        if reqId in RpcClientRspHandler.waitReqIdSet:
            RpcClientRspHandler.rpcQueryDBBarListRspDict[reqId] = rpcQueryDBBarListRsp
        else:
            logger.info("直接丢弃的回报,请求ID:%s", reqId)

