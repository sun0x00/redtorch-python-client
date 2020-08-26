import logging as logger
from threading import RLock
from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService


class RpcClientRspHandler:
    __waitReqIdSet = set()
    __waitReqIdSetLock = RLock()

    __rpcSubscribeRspDict = dict()
    __rpcSubscribeRspDictLock = RLock()

    __rpcUnsubscribeRspDict = dict()
    __rpcUnsubscribeRspDictLock = RLock()

    __rpcSubmitOrderRspDict = dict()
    __rpcSubmitOrderRspDictLock = RLock()

    __rpcCancelOrderRspDict = dict()
    __rpcCancelOrderRspDictLock = RLock()

    __rpcSearchContractRspDict = dict()
    __rpcSearchContractRspDictLock = RLock()

    __rpcExceptionRspDict = dict()
    __rpcExceptionRspDictLock = RLock()

    __rpcGetMixContractListRspDict = dict()
    __rpcGetMixContractListRspDictLock = RLock()

    __rpcGetPositionListRspDict = dict()
    __rpcGetPositionListRspDictLock = RLock()

    __rpcGetTradeListRspDict = dict()
    __rpcGetTradeListRspDictLock = RLock()

    __rpcGetOrderListRspDict = dict()
    __rpcGetOrderListRspDictLock = RLock()

    __rpcGetTickListRspDict = dict()
    __rpcGetTickListRspDictLock = RLock()

    __rpcGetAccountListRspDict = dict()
    __rpcGetAccountListRspDictLock = RLock()

    __rpcQueryDBBarListRspDict = dict()
    __rpcQueryDBBarListRspDictLock = RLock()

    @staticmethod
    def getAndRemoveRpcSubscribeRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcSubscribeRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcSubscribeRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcSubscribeRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcSubscribeRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcUnsubscribeRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcUnsubscribeRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcUnsubscribeRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcUnsubscribeRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcUnsubscribeRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcSubmitOrderRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcSubmitOrderRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcSubmitOrderRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcSubmitOrderRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcSubmitOrderRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcCancelOrderRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcCancelOrderRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcCancelOrderRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcCancelOrderRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcCancelOrderRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcSearchContractRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcSearchContractRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcSearchContractRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcSearchContractRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcSearchContractRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcExceptionRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcExceptionRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcExceptionRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcExceptionRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcExceptionRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcGetMixContractListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetMixContractListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcGetMixContractListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcGetMixContractListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetMixContractListRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcGetPositionListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetPositionListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcGetPositionListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcGetPositionListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetPositionListRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcGetTradeListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetTradeListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcGetTradeListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcGetTradeListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetTradeListRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcGetOrderListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetOrderListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcGetOrderListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcGetOrderListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetOrderListRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcGetTickListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetTickListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcGetTickListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcGetTickListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetTickListRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcQueryDBBarListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcQueryDBBarListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcQueryDBBarListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcQueryDBBarListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcQueryDBBarListRspDictLock.release()

    @staticmethod
    def getAndRemoveRpcGetAccountListRsp(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetAccountListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__rpcGetAccountListRspDict:
                if reqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__waitReqIdSet.remove(reqId)
                return RpcClientRspHandler.__rpcGetAccountListRspDict.pop(reqId)
            else:
                return None
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetAccountListRspDictLock.release()

    @staticmethod
    def registerWaitReqId(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        try:
            RpcClientRspHandler.__waitReqIdSet.add(reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()

    @staticmethod
    def unregisterWaitReqId(reqId):
        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        try:
            RpcClientRspHandler.__waitReqIdSet.remove(reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()

    @staticmethod
    def onSubscribeRsp(rpcSubscribeRsp):
        reqId = rpcSubscribeRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcSubscribeRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcSubscribeRspDict[reqId] = rpcSubscribeRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcSubscribeRspDictLock.release()

    @staticmethod
    def onUnsubscribeRsp(rpcUnsubscribeRsp):
        reqId = rpcUnsubscribeRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcUnsubscribeRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcUnsubscribeRspDict[reqId] = rpcUnsubscribeRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcUnsubscribeRspDictLock.release()

    @staticmethod
    def onSubmitOrderRsp(rpcSubmitOrderRsp):
        reqId = rpcSubmitOrderRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcSubmitOrderRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcSubmitOrderRspDict[reqId] = rpcSubmitOrderRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcSubmitOrderRspDictLock.release()

    @staticmethod
    def onCancelOrderRsp(rpcCancelOrderRsp):
        reqId = rpcCancelOrderRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcCancelOrderRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcCancelOrderRspDict[reqId] = rpcCancelOrderRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcCancelOrderRspDictLock.release()

    @staticmethod
    def onSearchContractRsp(rpcSearchContractRsp):
        reqId = rpcSearchContractRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcSearchContractRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcSearchContractRspDict[reqId] = rpcSearchContractRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcSearchContractRspDictLock.release()

    @staticmethod
    def onGetMixContractListRsp(rpcGetMixContractListRsp):
        reqId = rpcGetMixContractListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetMixContractListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcGetMixContractListRspDict[reqId] = rpcGetMixContractListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetMixContractListRspDictLock.release()

        if rpcGetMixContractListRsp.contract:
            ClientTradeCacheService.storeContractList(rpcGetMixContractListRsp.contract)

    @staticmethod
    def onGetAccountListRsp(rpcGetAccountListRsp):
        reqId = rpcGetAccountListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetAccountListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcGetAccountListRspDict[reqId] = rpcGetAccountListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetAccountListRspDictLock.release()

        if rpcGetAccountListRsp.account:
            ClientTradeCacheService.storeAccountList(rpcGetAccountListRsp.account)

    @staticmethod
    def onGetPositionListRsp(rpcGetPositionListRsp):
        reqId = rpcGetPositionListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetPositionListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcGetPositionListRspDict[reqId] = rpcGetPositionListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetPositionListRspDictLock.release()

        if rpcGetPositionListRsp.position:
            ClientTradeCacheService.storePositionList(rpcGetPositionListRsp.position)

    @staticmethod
    def onGetTradeListRsp(rpcGetTradeListRsp):
        reqId = rpcGetTradeListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetTradeListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcGetTradeListRspDict[reqId] = rpcGetTradeListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)

        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetTradeListRspDictLock.release()

        if rpcGetTradeListRsp.trade:
            ClientTradeCacheService.storeTradeList(rpcGetTradeListRsp.trade)

    @staticmethod
    def onGetOrderListRsp(rpcGetOrderListRsp):
        reqId = rpcGetOrderListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetOrderListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcGetOrderListRspDict[reqId] = rpcGetOrderListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetOrderListRspDictLock.release()

        if rpcGetOrderListRsp.order:
            ClientTradeCacheService.storeOrderList(rpcGetOrderListRsp.order)

    @staticmethod
    def onGetTickListRsp(rpcGetTickListRsp):
        reqId = rpcGetTickListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcGetTickListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcGetTickListRspDict[reqId] = rpcGetTickListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)

        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcGetTickListRspDictLock.release()

        if rpcGetTickListRsp.tick:
            ClientTradeCacheService.storeTickList(rpcGetTickListRsp.tick)

    @staticmethod
    def onExceptionRsp(rpcExceptionRsp):
        if rpcExceptionRsp.originalReqId:
            RpcClientRspHandler.__waitReqIdSetLock.acquire()
            RpcClientRspHandler.__rpcExceptionRspDictLock.acquire()
            try:
                logger.error("接收到异常回报,请求ID:%s,异常信息:%s", rpcExceptionRsp.originalReqId, rpcExceptionRsp.info)
                if rpcExceptionRsp.originalReqId in RpcClientRspHandler.__waitReqIdSet:
                    RpcClientRspHandler.__rpcExceptionRspDict[rpcExceptionRsp.originalReqId] = rpcExceptionRsp
            finally:
                RpcClientRspHandler.__waitReqIdSetLock.release()
                RpcClientRspHandler.__rpcExceptionRspDictLock.release()
        else:
            logger.error("接收到未知请求ID的异常回报,异常信息:%s", rpcExceptionRsp.info)

    @staticmethod
    def onQueryDBBarListRsp(rpcQueryDBBarListRsp):
        reqId = rpcQueryDBBarListRsp.commonRsp.reqId

        RpcClientRspHandler.__waitReqIdSetLock.acquire()
        RpcClientRspHandler.__rpcQueryDBBarListRspDictLock.acquire()
        try:
            if reqId in RpcClientRspHandler.__waitReqIdSet:
                RpcClientRspHandler.__rpcQueryDBBarListRspDict[reqId] = rpcQueryDBBarListRsp
            else:
                logger.info("直接丢弃的回报,请求ID:%s", reqId)
        finally:
            RpcClientRspHandler.__waitReqIdSetLock.release()
            RpcClientRspHandler.__rpcQueryDBBarListRspDictLock.release()
