import logging as logger
import time
import uuid

from xyz.redtorch.client.RtConfig import RtConfig
from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
from xyz.redtorch.client.service.rpc.RpcClientRspHandler import RpcClientRspHandler as RspHandler
from xyz.redtorch.pb.core_field_pb2 import CommonReqField, CancelOrderReqField
from xyz.redtorch.pb.core_rpc_pb2 import RpcId, RpcSubscribeReq, RpcUnsubscribeReq, RpcSubmitOrderReq, \
    RpcCancelOrderReq, RpcSearchContractReq, RpcGetAccountListReq, RpcGetMixContractListReq, RpcGetPositionListReq, \
    RpcGetOrderListReq, RpcGetTradeListReq, RpcGetTickListReq, RpcQueryDBBarListReq, RpcExceptionRsp, RpcSubscribeRsp, \
    RpcUnsubscribeRsp, RpcSubmitOrderRsp, RpcCancelOrderRsp, RpcSearchContractRsp, RpcGetAccountListRsp, \
    RpcGetMixContractListRsp, RpcGetPositionListRsp, RpcGetOrderListRsp, RpcGetTradeListRsp, RpcGetTickListRsp, \
    RpcQueryDBBarListRsp


class RpcClientApiService:
    subscribedContractDict = {}

    @staticmethod
    def subscribe(contract, transactionId=None, sync=False, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcSubscribeReq = RpcSubscribeReq()

        rpcSubscribeReq.commonReq.CopyFrom(commonReq)
        rpcSubscribeReq.contract.CopyFrom(contract)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        sendResult = RpcClientProcessService.sendRpc(RpcId.SUBSCRIBE_REQ, transactionId,
                                                     rpcSubscribeReq.SerializeToString())

        if sync and not sendResult:
            RspHandler.unregisterTransactionId(transactionId)
            return

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("订阅错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return False

                        elif isinstance(rsp, RpcSubscribeRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                RpcClientApiService.subscribedContractDict[
                                    contract.unifiedSymbol + "@" + str(contract.gatewayId)] = contract
                                return True
                            else:
                                logger.error("订阅错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return False
                        else:
                            logger.error("订阅错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return False
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("订阅错误,业务ID: %s,等待回报超时", transactionId)
                    return False

    @staticmethod
    def unsubscribe(contract, transactionId=None, sync=False, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())
        operatorId = RtConfig.operatorId

        commonReq = CommonReqField()
        commonReq.operatorId = operatorId
        commonReq.transactionId = transactionId

        rpcUnsubscribeReq = RpcUnsubscribeReq()

        rpcUnsubscribeReq.commonReq.CopyFrom(commonReq)
        rpcUnsubscribeReq.contract.CopyFrom(contract)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        sendResult = RpcClientProcessService.sendRpc(RpcId.UNSUBSCRIBE_REQ, transactionId,
                                                     rpcUnsubscribeReq.SerializeToString())

        if sync and not sendResult:
            RspHandler.unregisterTransactionId(transactionId)
            return

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("取消订阅错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return False

                        elif isinstance(rsp, RpcUnsubscribeRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                if contract.unifiedSymbol + "@" + str(
                                        contract.gatewayId) in RpcClientApiService.subscribedContractDict.keys():
                                    del RpcClientApiService.subscribedContractDict[
                                        contract.unifiedSymbol + "@" + str(contract.gatewayId)]
                                RpcClientApiService.subscribedContractDict[
                                    contract.unifiedSymbol + "@" + str(contract.gatewayId)] = contract
                                return True
                            else:
                                logger.error("取消订阅错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return False
                        else:
                            logger.error("取消订阅错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return False
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("取消订阅错误,业务ID: %s,等待回报超时", transactionId)
                    return False

    @staticmethod
    def submitOrder(submitOrderReq, transactionId=None, sync=False, rpcTimeOut=RtConfig.defaultRpcTimeOut):

        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcSubmitOrderReq = RpcSubmitOrderReq()

        rpcSubmitOrderReq.commonReq.CopyFrom(commonReq)
        rpcSubmitOrderReq.submitOrderReq.CopyFrom(submitOrderReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        sendResult = RpcClientProcessService.sendRpc(RpcId.SUBMIT_ORDER_REQ, transactionId,
                                                     rpcSubmitOrderReq.SerializeToString())

        if sync and not sendResult:
            RspHandler.unregisterTransactionId(transactionId)
            return

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("提交定单错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcSubmitOrderRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.orderId
                            else:
                                logger.error("提交定单错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("提交定单错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("提交定单错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def cancelOrder(orderId=None, originOrderId=None, transactionId=None, sync=False,
                    rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        cancelOrderReq = CancelOrderReqField()
        if not orderId and not originOrderId:
            logger.error("定单ID和原始定单ID不可同时为空")
            return False
        if originOrderId:
            cancelOrderReq.originOrderId = originOrderId
        if orderId:
            cancelOrderReq.orderId = orderId

        rpcCancelOrderReq = RpcCancelOrderReq()
        rpcCancelOrderReq.commonReq.CopyFrom(commonReq)
        rpcCancelOrderReq.cancelOrderReq.CopyFrom(cancelOrderReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        sendResult = RpcClientProcessService.sendRpc(RpcId.CANCEL_ORDER_REQ, transactionId,
                                                     rpcCancelOrderReq.SerializeToString())

        if sync and not sendResult:
            RspHandler.unregisterTransactionId(transactionId)
            return

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("撤销定单错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return False

                        elif isinstance(rsp, RpcCancelOrderRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return True
                            else:
                                logger.error("撤销定单错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return False
                        else:
                            logger.error("撤销定单错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return False
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("撤销定单错误,业务ID: %s,等待回报超时", transactionId)
                    return False

    @staticmethod
    def searchContract(contract, transactionId=None, sync=False, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcSearchContractReq = RpcSearchContractReq()

        rpcSearchContractReq.commonReq.CopyFrom(commonReq)
        rpcSearchContractReq.contract.CopyFrom(contract)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        sendResult = RpcClientProcessService.sendRpc(RpcId.SEARCH_CONTRACT_REQ, transactionId,
                                                     rpcSearchContractReq.SerializeToString())

        if sync and not sendResult:
            RspHandler.unregisterTransactionId(transactionId)
            return False

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("搜寻合约错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return False

                        elif isinstance(rsp, RpcSearchContractRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return True
                            else:
                                logger.error("搜寻合约错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return False
                        else:
                            logger.error("搜寻合约错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return False
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("搜寻合约错误,业务ID: %s,等待回报超时", transactionId)
                    return False

    @staticmethod
    def getAccountList(transactionId=None, sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcGetAccountListReq = RpcGetAccountListReq()

        rpcGetAccountListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.GET_ACCOUNT_LIST_REQ, transactionId,
                                                 rpcGetAccountListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取账户列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcGetAccountListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.account
                            else:
                                logger.error("获取账户列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取账户列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取账户列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def getMixContractList(transactionId=None, sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcGetMixContractListReq = RpcGetMixContractListReq()

        rpcGetMixContractListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.GET_MIX_CONTRACT_LIST_REQ, transactionId,
                                                 rpcGetMixContractListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取混合合约列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcGetMixContractListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.contract
                            else:
                                logger.error("获取混合合约列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取混合合约列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取混合合约列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def getPositionList(transactionId=None, sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcGetPositionListReq = RpcGetPositionListReq()

        rpcGetPositionListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.GET_POSITION_LIST_REQ, transactionId,
                                                 rpcGetPositionListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取持仓列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcGetPositionListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.position
                            else:
                                logger.error("获取持仓列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取持仓列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取持仓列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def getOrderList(transactionId=None, sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcGetOrderListReq = RpcGetOrderListReq()

        rpcGetOrderListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.GET_ORDER_LIST_REQ, transactionId,
                                                 rpcGetOrderListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取定单列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcGetOrderListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.order
                            else:
                                logger.error("获取定单列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取定单列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取定单列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def getTradeList(transactionId=None, sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcGetTradeListReq = RpcGetTradeListReq()

        rpcGetTradeListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.GET_TRADE_LIST_REQ, transactionId,
                                                 rpcGetTradeListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取成交列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcGetTradeListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.trade
                            else:
                                logger.error("获取成交列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取成交列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取成交列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def getTickList(transactionId=None, sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcGetTickListReq = RpcGetTickListReq()

        rpcGetTickListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.GET_TICK_LIST_REQ, transactionId,
                                                 rpcGetTickListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取Tick列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcGetTickListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.tick
                            else:
                                logger.error("获取Tick列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取Tick列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取Tick列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None

    @staticmethod
    def queryDBBarList(startTimestamp, endTimestamp, unifiedSymbol, barPeriod, marketDataDBType, transactionId=None,
                       sync=True, rpcTimeOut=RtConfig.defaultRpcTimeOut):
        if not transactionId:
            transactionId = str(uuid.uuid4())

        commonReq = CommonReqField()
        commonReq.operatorId = RtConfig.operatorId
        commonReq.transactionId = transactionId

        rpcQueryDBBarListReq = RpcQueryDBBarListReq()

        rpcQueryDBBarListReq.commonReq.CopyFrom(commonReq)

        rpcQueryDBBarListReq.startTimestamp = startTimestamp
        rpcQueryDBBarListReq.endTimestamp = endTimestamp
        rpcQueryDBBarListReq.unifiedSymbol = unifiedSymbol
        rpcQueryDBBarListReq.barPeriod = barPeriod
        rpcQueryDBBarListReq.marketDataDBType = marketDataDBType

        if sync:
            RspHandler.registerTransactionId(transactionId)

        RpcClientProcessService.sendAsyncHttpRpc(RpcId.QUERY_DB_BAR_LIST_REQ, transactionId,
                                                 rpcQueryDBBarListReq.SerializeToString())

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < rpcTimeOut:
                    if not RspHandler.containsTransactionId(transactionId):
                        return False
                    rsp = RspHandler.getAndRemoveRpcRsp(transactionId)
                    if rsp:
                        if isinstance(rsp, RpcExceptionRsp):
                            logger.error("获取Bar列表错误,业务ID: %s, 远程错误回报 %s", transactionId, rsp.info)
                            return None

                        elif isinstance(rsp, RpcQueryDBBarListRsp):
                            commonRsp = rsp.commonRsp
                            errorId = commonRsp.errorId
                            if errorId == 0:
                                return rsp.bar
                            else:
                                logger.error("获取Bar列表错误,业务ID:%s,错误ID:%s,远程错误回报:%s", transactionId, errorId,
                                             commonRsp.errorMsg)
                                return None
                        else:
                            logger.error("获取Bar列表错误,业务ID:%s,远程回报数据类型错误", transactionId)
                            return None
                    else:
                        time.sleep(0.02)
                else:
                    RspHandler.unregisterTransactionId(transactionId)
                    logger.error("获取Bar列表错误,业务ID: %s,等待回报超时", transactionId)
                    return None
