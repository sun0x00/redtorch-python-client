import base64
import json
import logging as logger
import time
from concurrent.futures.thread import ThreadPoolExecutor

import lz4framed
import requests

from xyz.redtorch.client.RtConfig import RtConfig
from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService
from xyz.redtorch.client.service.rpc.RpcClientRspHandler import RpcClientRspHandler
from xyz.redtorch.client.service.rpc.RpcClientRtnHandler import RpcClientRtnHandler
from xyz.redtorch.client.web.socket.WebSocketClientHandler import WebSocketClientHandler
from xyz.redtorch.pb.core_rpc_pb2 import RpcSubmitOrderRsp, RpcExceptionRsp, RpcId, RpcCancelOrderRsp, \
    RpcSubscribeRsp, RpcUnsubscribeRsp, RpcSearchContractRsp, RpcGetContractListRsp, RpcGetTickListRsp, \
    RpcGetOrderListRsp, RpcGetTradeListRsp, RpcGetPositionListRsp, RpcPositionRtn, RpcOrderRtn, \
    RpcTradeRtn, RpcAccountRtn, RpcNoticeRtn, RpcTickRtn, RpcContractRtn, RpcGetAccountListRsp, \
    RpcOrderListRtn, RpcTradeListRtn, RpcContractListRtn, RpcPositionListRtn, RpcAccountListRtn, \
    RpcTickListRtn, RpcQueryDBBarListRsp
from xyz.redtorch.pb.dep_pb2 import DataExchangeProtocol


class RpcClientProcessService:
    asyncHttpRpcExecutor = ThreadPoolExecutor(max_workers=5)
    importantExecutor = ThreadPoolExecutor(max_workers=999)
    normalExecutor = ThreadPoolExecutor(max_workers=5)
    unimportantSingleThreadExecutor = ThreadPoolExecutor(max_workers=1)
    tradeRtnQueueSingleExecutor = ThreadPoolExecutor(max_workers=1)
    marketRtnQueueSingleExecutor = ThreadPoolExecutor(max_workers=1)

    @staticmethod
    def processData(data):
        try:
            dep = DataExchangeProtocol()
            dep.ParseFromString(data)
        except:
            logger.error("处理DEP错误,PB解析数据发生错误", exc_info=True)
            logger.error("处理DEP错误,PB解析数据发生错误,原始数据:%s", data)
            return

        rpcId = dep.rpcId
        timestamp = dep.timestamp
        contentType = dep.contentType

        if contentType == DataExchangeProtocol.ContentType.COMPRESSED_LZ4:
            try:
                contentByteString = lz4framed.decompress(dep.contentBytes)
            except:
                logger.error("处理DEP异常,RPC ID:%s,内容类型:%s,时间戳:%s,无法使用LZ4正确解析报文内容", rpcId, timestamp, contentType,
                             exc_info=True)
                return
        elif contentType == DataExchangeProtocol.ContentType.ROUTINE:
            contentByteString = dep.contentBytes
        else:
            logger.error("处理DEP异常,RPC ID:%s,内容类型:%s,时间戳:%s,不支持的报文类型", rpcId, timestamp, contentType)
            return

        if not contentByteString or len(contentByteString) <= 0:
            logger.error("处理DEP异常,RPC ID:%s,内容类型:%s,时间戳:%s,报文长度错误", rpcId, timestamp, contentType)
            return

        RpcClientProcessService.doCoreRpc(rpcId, contentByteString, timestamp)

    @staticmethod
    def doCoreRpc(rpcId, contentByteString, timestamp):

        cls = RpcClientProcessService

        if rpcId == RpcId.UNKNOWN_RPC_ID:
            logger.warning("处理RPC,未知RPC ID:%s", rpcId)
            return
        elif rpcId == RpcId.SUBSCRIBE_RSP:
            def process():
                transactionId = ""
                try:
                    rpcSubscribeRsp = RpcSubscribeRsp()
                    rpcSubscribeRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcSubscribeRsp.commonRsp)
                    transactionId = rpcSubscribeRsp.commonRsp.transactionId
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcSubscribeRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:SUBSCRIBE_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.UNSUBSCRIBE_RSP:
            def process():
                transactionId = ""
                try:
                    rpcUnsubscribeRsp = RpcUnsubscribeRsp()
                    rpcUnsubscribeRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcUnsubscribeRsp.commonRsp)
                    transactionId = rpcUnsubscribeRsp.commonRsp.transactionId
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcUnsubscribeRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:UNSUBSCRIBE_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.SUBMIT_ORDER_RSP:
            def process():
                transactionId = ""
                try:
                    rpcSubmitOrderRsp = RpcSubmitOrderRsp()
                    rpcSubmitOrderRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcSubmitOrderRsp.commonRsp)
                    transactionId = rpcSubmitOrderRsp.commonRsp.transactionId
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcSubmitOrderRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:SUBMIT_ORDER_RSP", transactionId, exc_info=True)

            cls.importantExecutor.submit(process)
        elif rpcId == RpcId.CANCEL_ORDER_RSP:
            def process():
                transactionId = ""
                try:
                    rpcCancelOrderRsp = RpcCancelOrderRsp()
                    rpcCancelOrderRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcCancelOrderRsp.commonRsp)
                    transactionId = rpcCancelOrderRsp.commonRsp.transactionId
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcCancelOrderRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:CANCEL_ORDER_RSP", transactionId, exc_info=True)

            cls.importantExecutor.submit(process)

        elif rpcId == RpcId.SEARCH_CONTRACT_RSP:
            def process():
                transactionId = ""
                try:
                    rpcSearchContractRsp = RpcSearchContractRsp()
                    rpcSearchContractRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcSearchContractRsp.commonRsp)
                    transactionId = rpcSearchContractRsp.commonRsp.transactionId
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcSearchContractRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:SEARCH_CONTRACT_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.GET_CONTRACT_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcGetContractListRsp = RpcGetContractListRsp()
                    rpcGetContractListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcGetContractListRsp.commonRsp)
                    transactionId = rpcGetContractListRsp.commonRsp.transactionId
                    ClientTradeCacheService.storeContractList(rpcGetContractListRsp.contract)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcGetContractListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:GET_CONTRACT_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.GET_TICK_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcGetTickListRsp = RpcGetTickListRsp()
                    rpcGetTickListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcGetTickListRsp.commonRsp)
                    transactionId = rpcGetTickListRsp.commonRsp.transactionId
                    ClientTradeCacheService.storeTickList(rpcGetTickListRsp.tick)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcGetTickListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:GET_TICK_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.GET_POSITION_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcGetPositionListRsp = RpcGetPositionListRsp()
                    rpcGetPositionListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcGetPositionListRsp.commonRsp)
                    transactionId = rpcGetPositionListRsp.commonRsp.transactionId
                    ClientTradeCacheService.storePositionList(rpcGetPositionListRsp.position)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcGetPositionListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:GET_POSITION_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.GET_ACCOUNT_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcGetAccountListRsp = RpcGetAccountListRsp()
                    rpcGetAccountListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcGetAccountListRsp.commonRsp)
                    transactionId = rpcGetAccountListRsp.commonRsp.transactionId
                    ClientTradeCacheService.storeAccountList(rpcGetAccountListRsp.account)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcGetAccountListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:GET_ACCOUNT_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.GET_TRADE_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcGetTradeListRsp = RpcGetTradeListRsp()
                    rpcGetTradeListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcGetTradeListRsp.commonRsp)
                    transactionId = rpcGetTradeListRsp.commonRsp.transactionId
                    ClientTradeCacheService.storeTradeList(rpcGetTradeListRsp.trade)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcGetTradeListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:GET_TRADE_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.GET_ORDER_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcGetOrderListRsp = RpcGetOrderListRsp()
                    rpcGetOrderListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcGetOrderListRsp.commonRsp)
                    transactionId = rpcGetOrderListRsp.commonRsp.transactionId
                    ClientTradeCacheService.storeOrderList(rpcGetOrderListRsp.order)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcGetOrderListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:GET_ORDER_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)
        elif rpcId == RpcId.QUERY_DB_BAR_LIST_RSP:
            def process():
                transactionId = ""
                try:
                    rpcQueryDBBarListRsp = RpcQueryDBBarListRsp()
                    rpcQueryDBBarListRsp.ParseFromString(contentByteString)
                    cls.checkCommonRsp(rpcQueryDBBarListRsp.commonRsp)
                    transactionId = rpcQueryDBBarListRsp.commonRsp.transactionId
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcQueryDBBarListRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:QUERY_DB_BAR_LIST_RSP", transactionId, exc_info=True)

            cls.normalExecutor.submit(process)

        elif rpcId == RpcId.EXCEPTION_RSP:
            def process():
                transactionId = ""
                try:
                    rpcExceptionRsp = RpcExceptionRsp()
                    rpcExceptionRsp.ParseFromString(contentByteString)
                    transactionId = rpcExceptionRsp.originalTransactionId
                    logger.info("处理RPC记录,业务ID:%s,业务ID:%s,RPC:EXCEPTION_RSP", transactionId, transactionId)
                    RpcClientRspHandler.onRpcRsp(transactionId, rpcExceptionRsp)
                except:
                    logger.error("处理RPC异常,业务ID:%s,RPC:EXCEPTION_RSP", transactionId, exc_info=True)

            cls.importantExecutor.submit(process)
        ###################################
        elif rpcId == RpcId.ORDER_RTN:
            def process():
                try:
                    rpcOrderRtn = RpcOrderRtn()
                    rpcOrderRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcOrderRtn(rpcOrderRtn)
                except:
                    logger.error("处理RPC异常,RPC:ORDER_RTN", exc_info=True)

            cls.tradeRtnQueueSingleExecutor.submit(process)

        elif rpcId == RpcId.TRADE_RTN:
            def process():
                try:
                    rpcTradeRtn = RpcTradeRtn()
                    rpcTradeRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcTradeRtn(rpcTradeRtn)
                except:
                    logger.error("处理RPC异常,RPC:TRADE_RTN", exc_info=True)

            cls.tradeRtnQueueSingleExecutor.submit(process)
        elif rpcId == RpcId.POSITION_RTN:
            def process():
                try:
                    rpcPositionRtn = RpcPositionRtn()
                    rpcPositionRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcPositionRtn(rpcPositionRtn)
                except:
                    logger.error("处理RPC异常,RPC:POSITION_RTN", exc_info=True)

            cls.tradeRtnQueueSingleExecutor.submit(process)

        elif rpcId == RpcId.ACCOUNT_RTN:
            def process():
                try:
                    rpcAccountRtn = RpcAccountRtn()
                    rpcAccountRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcAccountRtn(rpcAccountRtn)
                except:
                    logger.error("处理RPC异常,RPC:ACCOUNT_RTN", exc_info=True)

            cls.tradeRtnQueueSingleExecutor.submit(process)

        elif rpcId == RpcId.CONTRACT_RTN:
            def process():
                try:
                    rpcContractRtn = RpcContractRtn()
                    rpcContractRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcContractRtn(rpcContractRtn)
                except:
                    logger.error("处理RPC异常,RPC:CONTRACT_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)
        elif rpcId == RpcId.NOTICE_RTN:
            def process():
                try:
                    rpcNoticeRtn = RpcNoticeRtn()
                    rpcNoticeRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcNoticeRtn(rpcNoticeRtn)
                except:
                    logger.error("处理RPC异常,RPC:NOTICE_RTN", exc_info=True)

            cls.tradeRtnQueueSingleExecutor.submit(process)
        elif rpcId == RpcId.TICK_RTN:
            def process():
                try:
                    rpcTickRtn = RpcTickRtn()
                    rpcTickRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcTickRtn(rpcTickRtn)
                except:
                    logger.error("处理RPC异常,RPC:TICK_RTN", exc_info=True)

            cls.marketRtnQueueSingleExecutor.submit(process)

        elif rpcId == RpcId.ORDER_LIST_RTN:
            def process():
                try:
                    rpcOrderListRtn = RpcOrderListRtn()
                    rpcOrderListRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcOrderListRtn(rpcOrderListRtn)
                except:
                    logger.error("处理RPC异常,RPC:ORDER_LIST_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)

        elif rpcId == RpcId.TRADE_LIST_RTN:
            def process():
                try:
                    rpcTradeListRtn = RpcTradeListRtn()
                    rpcTradeListRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcTradeListRtn(rpcTradeListRtn)
                except:
                    logger.error("处理RPC异常,RPC:TRADE_LIST_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)
        elif rpcId == RpcId.CONTRACT_LIST_RTN:
            def process():
                try:
                    rpcContractListRtn = RpcContractListRtn()
                    rpcContractListRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcContractListRtn(rpcContractListRtn)
                except:
                    logger.error("处理RPC异常,RPC:CONTRACT_LIST_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)
        elif rpcId == RpcId.POSITION_LIST_RTN:
            def process():
                try:
                    rpcPositionListRtn = RpcPositionListRtn()
                    rpcPositionListRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcPositionListRtn(rpcPositionListRtn)
                except:
                    logger.error("处理RPC异常,RPC:POSITION_LIST_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)
        elif rpcId == RpcId.ACCOUNT_LIST_RTN:
            def process():
                try:
                    rpcAccountListRtn = RpcAccountListRtn()
                    rpcAccountListRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcAccountListRtn(rpcAccountListRtn)
                except:
                    logger.error("处理RPC异常,RPC:ACCOUNT_LIST_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)
        elif rpcId == RpcId.TICK_LIST_RTN:
            def process():
                try:
                    rpcTickListRtn = RpcTickListRtn()
                    rpcTickListRtn.ParseFromString(contentByteString)
                    RpcClientRtnHandler.onRpcTickListRtn(rpcTickListRtn)
                except:
                    logger.error("处理RPC异常,RPC:TICK_LIST_RTN", exc_info=True)

            cls.unimportantSingleThreadExecutor.submit(process)

        else:
            logger.error("处理RPC错误, 来源节点ID:%s, 业务ID:%s 不支持此功能", rpcId)

    @staticmethod
    def checkCommonRsp(commonRsp):
        if not commonRsp:
            logger.error("参数commonRsp缺失")
            raise Exception("参数commonRsp缺失")

    @staticmethod
    def sendRpc(rpcId, transactionId, content):
        data = RpcClientProcessService.generateRpcDep(rpcId, transactionId, content)
        if data:
            return WebSocketClientHandler.sendData(data)
        return False

    @staticmethod
    def sendAsyncHttpRpc(rpcId, transactionId, content):

        def process():
            try:
                data = RpcClientProcessService.generateRpcDep(rpcId, transactionId, content)
                if data:
                    base64Str = base64.b64encode(data).decode('ascii')
                    payload = {
                        'voData': base64Str
                    }
                    headers = {'Auth-Token': RtConfig.authToken, "content-type": "application/json"}
                    response = requests.post(RtConfig.rpcUri, data=json.dumps(payload), headers=headers)
                    if response.status_code == 200:
                        ret = response.json()
                        if ret['status']:
                            rspBase64Str = ret['voData']
                            if rspBase64Str:
                                rspData = base64.b64decode(rspBase64Str)
                                RpcClientProcessService.processData(rspData)
                            else:
                                RpcClientRspHandler.unregisterTransactionId(transactionId)
                        else:
                            logger.error("HTTP RPC错误,业务ID:%s,RPC:%s,信息:%s", transactionId, rpcId, ret.message)
                            RpcClientRspHandler.unregisterTransactionId(transactionId)
                    else:
                        logger.error("HTTP RPC错误,返回非200状态码,业务ID:%s,RPC:%s,状态码:%s", transactionId, rpcId,
                                     str(response.status_code))
                        RpcClientRspHandler.unregisterTransactionId(transactionId)
                else:
                    RpcClientRspHandler.unregisterTransactionId(transactionId)
            except:
                logger.error("HTTP RPC错误,业务ID:%s,RPC:%s", transactionId, rpcId, exc_info=True)
                RpcClientRspHandler.unregisterTransactionId(transactionId)

        RpcClientProcessService.asyncHttpRpcExecutor.submit(process)

    @staticmethod
    def onWsClosed():
        pass

    @staticmethod
    def onWsError():
        pass

    @staticmethod
    def onWsConnected():
        time.sleep(2)
        from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService
        for contract in RpcClientApiService.subscribedContractDict.values():
            RpcClientApiService.subscribe(contract)

    @staticmethod
    def generateRpcDep(rpcId, transactionId, content):
        if content:
            if len(content) > 10240:
                return RpcClientProcessService.generateRoutineRpcDep(rpcId, content)
            else:
                return RpcClientProcessService.generateLz4RpcDep(rpcId, transactionId, content)
        else:
            logger.error("发送RPC记录错误,内容为空,业务ID:%s,RPC ID:%s", transactionId, rpcId)
            return None

    @staticmethod
    def generateRoutineRpcDep(rpcId, content):
        dep = DataExchangeProtocol()
        dep.contentType = DataExchangeProtocol.ContentType.ROUTINE
        dep.rpcId = rpcId
        dep.contentBytes = content
        dep.timestamp = int(round(time.time() * 1000))

        return dep.SerializeToString()

    @staticmethod
    def generateLz4RpcDep(rpcId, transactionId, content):
        try:
            encodeContent = lz4framed.compress(content)
        except:
            logger.error("发送RPC错误,压缩错误,业务ID:%s,RPC ID:%s", transactionId, rpcId, exc_info=True)
            return False

        dep = DataExchangeProtocol()
        dep.contentType = DataExchangeProtocol.ContentType.COMPRESSED_LZ4
        dep.rpcId = rpcId
        dep.contentBytes = encodeContent
        dep.timestamp = int(round(time.time() * 1000))

        return dep.SerializeToString()
