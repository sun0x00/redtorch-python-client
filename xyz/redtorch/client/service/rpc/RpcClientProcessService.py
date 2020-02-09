from xyz.redtorch.pb.dep_pb2 import DataExchangeProtocol
from xyz.redtorch.pb.core_rpc_pb2 import RpcSubmitOrderRsp, RpcExceptionRsp, RpcId, RpcCancelOrderRsp, \
    RpcSubscribeRsp, RpcUnsubscribeRsp, RpcSearchContractRsp, RpcGetMixContractListRsp, RpcGetTickListRsp, \
    RpcGetOrderListRsp, RpcGetTradeListRsp, RpcGetPositionListRsp, RpcPositionRtn, RpcOrderRtn, \
    RpcTradeRtn, RpcAccountRtn, RpcNoticeRtn, RpcTickRtn, RpcContractRtn, RpcGetAccountListRsp, \
    RpcOrderListRtn, RpcTradeListRtn, RpcContractListRtn, RpcPositionListRtn, RpcAccountListRtn, \
    RpcTickListRtn
from xyz.redtorch.client.Config import Config
from xyz.redtorch.client.service.rpc.RpcClientRspHandler import RpcClientRspHandler
from xyz.redtorch.client.service.rpc.RpcClientRtnHandler import RpcClientRtnHandler
from xyz.redtorch.client.web.socket.WebSocketClientHandler import WebSocketClientHandler
import logging as logger
import lz4framed
import time


class RpcClientProcessService:
    @staticmethod
    def processData(data):
        try:
            dep = DataExchangeProtocol()
            dep.ParseFromString(data)

        except Exception as e:
            logger.error("处理DEP错误,PB解析数据发生错误")
            logger.error(e, exc_info=True)
            logger.error("处理DEP错误,PB解析数据发生错误,原始数据:%s", data)
            return

        sourceNodeId = dep.sourceNodeId
        targetNodeId = dep.targetNodeId

        if targetNodeId != Config.nodeId:
            logger.error("处理DEP错误,目标节点ID不匹配当前节点ID:%s,目标节点ID:%s", Config.nodeId, targetNodeId)
            return

        rpcId = dep.rpcId
        timestamp = dep.timestamp
        contentType = dep.contentType
        rpcType = dep.rpcType
        reqId = dep.reqId
        logger.info("处理DEP记录,来源节点ID:%s,RPC类型:%s,RPC ID:%s,请求ID:%s内容类型:%s,时间戳:%s", sourceNodeId,
                    rpcType, rpcId, reqId, contentType, timestamp)

        if contentType == DataExchangeProtocol.ContentType.COMPRESSED_LZ4:
            try:
                contentByteString = lz4framed.decompress(dep.contentBytes)
            except Exception as e:
                logger.error("处理DEP异常,来源节点ID:%s,RPC类型:%s,RPC ID:%s,请求ID:%s时间戳:%s,无法使用LZ4正确解析报文内容", sourceNodeId,
                             rpcType, rpcId, reqId, timestamp)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, "无法使用LZ4正确解析报文内容")
                return
        elif contentType == DataExchangeProtocol.ContentType.ROUTINE:
            contentByteString = dep.contentBytes
        else:
            logger.error("处理DEP错误，来源节点ID:%s,RPC类型:%s,RPC ID:%s,请求ID:%s内容类型:%s,时间戳:%s,不支持的报文类型", sourceNodeId,
                         rpcType, rpcId, reqId, contentType, timestamp)
            RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, "不支持的报文类型")
            return

        if not contentByteString or len(contentByteString) <= 0:
            logger.error("处理DEP错误，来源节点ID:%s,RPC类型:%s,RPC ID:%s,请求ID:%s内容类型:%s,时间戳:%s,报文内容长度错误", sourceNodeId,
                         rpcType, rpcId, contentType, timestamp)
            RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, "报文内容长度错误")
            return

        if rpcType != DataExchangeProtocol.RpcType.CORE_RPC:
            logger.error("处理DEP错误，来源节点ID:%s,RPC类型:%s,RPC ID:%s,请求ID:%s内容类型:%s,时间戳:%s,未能识别的RPC类型", sourceNodeId,
                         rpcType, rpcId, reqId, contentType, timestamp)
            return

        RpcClientProcessService.doCoreRpc(sourceNodeId, rpcId, reqId, contentByteString, timestamp)

    @staticmethod
    def doCoreRpc(sourceNodeId, rpcId, reqId, contentByteString, timestamp):
        if rpcId == RpcId.UNKNOWN_RPC_ID:
            logger.warning("处理RPC,来源节点ID:%s,RPC ID:%s", sourceNodeId, rpcId)
            return
        elif rpcId == RpcId.SUBSCRIBE_RSP:
            try:
                rpcSubscribeRsp = RpcSubscribeRsp()
                rpcSubscribeRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcSubscribeRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:SUBSCRIBE_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onSubscribeRsp(rpcSubscribeRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:SUBSCRIBE_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.UNSUBSCRIBE_RSP:
            try:
                rpcUnsubscribeRsp = RpcUnsubscribeRsp()
                rpcUnsubscribeRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcUnsubscribeRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:UNSUBSCRIBE_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onUnsubscribeRsp(rpcUnsubscribeRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:UNSUBSCRIBE_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.SUBMIT_ORDER_RSP:
            try:
                rpcSubmitOrderRsp = RpcSubmitOrderRsp()
                rpcSubmitOrderRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcSubmitOrderRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:SUBMIT_ORDER_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onSubmitOrderRsp(rpcSubmitOrderRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:SUBMIT_ORDER_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.CANCEL_ORDER_RSP:
            try:
                rpcCancelOrderRsp = RpcCancelOrderRsp()
                rpcCancelOrderRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcCancelOrderRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:CANCEL_ORDER_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onCancelOrderRsp(rpcCancelOrderRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:CANCEL_ORDER_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.SEARCH_CONTRACT_RSP:
            try:
                rpcSearchContractRsp = RpcSearchContractRsp()
                rpcSearchContractRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcSearchContractRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:SEARCH_CONTRACT_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onSearchContractRsp(rpcSearchContractRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:SEARCH_CONTRACT_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.GET_MIX_CONTRACT_LIST_RSP:
            try:
                rpcGetMixContractListRsp = RpcGetMixContractListRsp()
                rpcGetMixContractListRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcGetMixContractListRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:GET_MIX_CONTRACT_LIST_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onGetMixContractListRsp(rpcGetMixContractListRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:GET_MIX_CONTRACT_LIST_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.GET_POSITION_LIST_RSP:
            try:
                rpcGetPositionListRsp = RpcGetPositionListRsp()
                rpcGetPositionListRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcGetPositionListRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:GET_POSITION_LIST_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onGetPositionListRsp(rpcGetPositionListRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:GET_POSITION_LIST_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.GET_ACCOUNT_LIST_RSP:
            try:
                rpcGetAccountListRsp = RpcGetAccountListRsp()
                rpcGetAccountListRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcGetAccountListRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:GET_ACCOUNT_LIST_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onGetAccountListRsp(rpcGetAccountListRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:GET_ACCOUNT_LIST_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.GET_TRADE_LIST_RSP:
            try:
                rpcGetTradeListRsp = RpcGetTradeListRsp()
                rpcGetTradeListRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcGetTradeListRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:GET_TRADE_LIST_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onGetTradeListRsp(rpcGetTradeListRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:GET_TRADE_LIST_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.GET_ORDER_LIST_RSP:
            try:
                rpcGetOrderListRsp = RpcGetOrderListRsp()
                rpcGetOrderListRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcGetOrderListRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:GET_ORDER_LIST_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onGetOrderListRsp(rpcGetOrderListRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:GET_ORDER_LIST_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.GET_TICK_LIST_RSP:
            try:
                rpcGetTickListRsp = RpcGetTickListRsp()
                rpcGetTickListRsp.ParseFromString(contentByteString)
                RpcClientProcessService.checkCommonRsp(rpcGetTickListRsp.commonRsp, sourceNodeId, reqId)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:GET_TICK_LIST_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onGetTickListRsp(rpcGetTickListRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:GET_TICK_LIST_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        elif rpcId == RpcId.EXCEPTION_RSP:
            try:
                rpcExceptionRsp = RpcExceptionRsp()
                rpcExceptionRsp.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:EXCEPTION_RSP", sourceNodeId, reqId)
                RpcClientRspHandler.onExceptionRsp(rpcExceptionRsp)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:EXCEPTION_RSP", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.ORDER_RTN:
            try:
                rpcOrderRtn = RpcOrderRtn()
                rpcOrderRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:ORDER_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcOrderRtn(rpcOrderRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:ORDER_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.TRADE_RTN:
            try:
                rpcTradeRtn = RpcTradeRtn()
                rpcTradeRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:TRADE_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcTradeRtn(rpcTradeRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:TRADE_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.POSITION_RTN:
            try:
                rpcPositionRtn = RpcPositionRtn()
                rpcPositionRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:POSITION_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcPositionRtn(rpcPositionRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:POSITION_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.ACCOUNT_RTN:
            try:
                rpcAccountRtn = RpcAccountRtn()
                rpcAccountRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:ACCOUNT_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcAccountRtn(rpcAccountRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:ACCOUNT_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.CONTRACT_RTN:
            try:
                rpcContractRtn = RpcContractRtn()
                rpcContractRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:CONTRACT_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcContractRtn(rpcContractRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:CONTRACT_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.TICK_RTN:
            try:
                rpcTickRtn = RpcTickRtn()
                rpcTickRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:TICK_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcTickRtn(rpcTickRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:TICK_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.ORDER_LIST_RTN:
            try:
                rpcOrderListRtn = RpcOrderListRtn()
                rpcOrderListRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:ORDER_LIST_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcOrderListRtn(rpcOrderListRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:ORDER_LIST_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.TRADE_LIST_RTN:
            try:
                rpcTradeListRtn = RpcTradeListRtn()
                rpcTradeListRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:TRADE_LIST_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcTradeListRtn(rpcTradeListRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:TRADE_LIST_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.CONTRACT_LIST_RTN:
            try:
                rpcContractListRtn = RpcContractListRtn()
                rpcContractListRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:CONTRACT_LIST_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcContractListRtn(rpcContractListRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:CONTRACT_LIST_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.POSITION_LIST_RTN:
            try:
                rpcPositionListRtn = RpcPositionListRtn()
                rpcPositionListRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:POSITION_LIST_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcPositionListRtn(rpcPositionListRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:POSITION_LIST_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.ACCOUNT_LIST_RTN:
            try:
                rpcAccountListRtn = RpcAccountListRtn()
                rpcAccountListRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:ACCOUNT_LIST_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcAccountListRtn(rpcAccountListRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:ACCOUNT_LIST_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.TICK_LIST_RTN:
            try:
                rpcTickListRtn = RpcTickListRtn()
                rpcTickListRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:TICK_LIST_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcTickListRtn(rpcTickListRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:TICK_LIST_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))

        elif rpcId == RpcId.NOTICE_RTN:
            try:
                rpcNoticeRtn = RpcNoticeRtn()
                rpcNoticeRtn.ParseFromString(contentByteString)
                logger.info("处理RPC记录,来源节点ID:%s,请求ID:%s,RPC:NOTICE_RTN", sourceNodeId, reqId)
                RpcClientRtnHandler.onRpcNoticeRtn(rpcNoticeRtn)
            except Exception as e:
                logger.error("处理RPC异常,来源节点ID:%s,RPC:NOTICE_RTN", sourceNodeId)
                logger.error(e, exc_info=True)
                RpcClientProcessService.sendExceptionRsp(sourceNodeId, rpcId, reqId, timestamp, str(e))
        else:
            logger.error("处理RPC错误, 来源节点ID:%s, RPC ID:%s, 请求ID:%s 不支持此功能", sourceNodeId, rpcId, reqId);

    @staticmethod
    def checkCommonRsp(commonRsp, sourceNodeId, reqId):
        if not commonRsp:
            logger.error("参数commonRsp缺失")
            raise Exception("参数commonRsp缺失")

        if not commonRsp.reqId or commonRsp.reqId == "":
            logger.error("参数reqId缺失")
            raise Exception("参数reqId缺失")

        if commonRsp.reqId != reqId:
            logger.error("请求ID不匹配")
            raise Exception("请求ID不匹配")

    @staticmethod
    def sendExceptionRsp(targetNodeId, originalRpcId, originalReqId, originalTimestamp, info):
        rpcExceptionRsp = RpcExceptionRsp()
        rpcExceptionRsp.originalRpcId = originalRpcId
        rpcExceptionRsp.originalReqId = originalReqId
        rpcExceptionRsp.originalTimestamp = originalTimestamp
        rpcExceptionRsp.info = info

        RpcClientProcessService.sendRoutineCoreRpc(targetNodeId, rpcExceptionRsp.SerializeToString(), originalReqId,
                                                   RpcId.EXCEPTION_RSP)

    @staticmethod
    def sendCoreRpc(targetNodeId, content, reqId, rpcId):
        logger.info("发送RPC记录,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)
        if content:
            if len(content) > 262144:
                return RpcClientProcessService.sendRoutineCoreRpc(targetNodeId, content, reqId, rpcId)
            else:
                return RpcClientProcessService.sendLz4CoreRpc(targetNodeId, content, reqId, rpcId)
        else:
            logger.error("发送RPC记录错误,内容为空,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)

    @staticmethod
    def sendRoutineCoreRpc(targetNodeId, content, reqId, rpcId):
        logger.info("发送RPC记录,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)
        dep = DataExchangeProtocol()
        dep.contentType = DataExchangeProtocol.ContentType.ROUTINE
        dep.reqId = reqId
        dep.rpcType = DataExchangeProtocol.RpcType.CORE_RPC
        dep.rpcId = rpcId
        dep.sourceNodeId = Config.nodeId
        dep.targetNodeId = targetNodeId
        dep.timestamp = int(round(time.time() * 1000))
        dep.contentBytes = content

        if not WebSocketClientHandler.sendData(dep.SerializeToString()):
            logger.error("发送RPC错误,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)
            return False
        return True

    @staticmethod
    def sendLz4CoreRpc(targetNodeId, content, reqId, rpcId):
        logger.info("发送RPC记录,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)
        try:
            encodeContent = lz4framed.compress(content)
        except Exception as e:
            logger.error("发送RPC错误,压缩错误,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)
            logger.error(e, exc_info=True)
            return False

        dep = DataExchangeProtocol()
        dep.contentType = DataExchangeProtocol.ContentType.COMPRESSED_LZ4
        dep.reqId = reqId
        dep.rpcType = DataExchangeProtocol.RpcType.CORE_RPC
        dep.rpcId = rpcId
        dep.sourceNodeId = Config.nodeId
        dep.targetNodeId = targetNodeId
        dep.timestamp = int(round(time.time() * 1000))
        dep.contentBytes = encodeContent
        if not WebSocketClientHandler.sendData(dep.SerializeToString()):
            logger.error("发送RPC错误,目标节点:%s,请求ID:%s,RPC ID:%s", targetNodeId, reqId, rpcId)
            return False
        return True

    @staticmethod
    def onWsClosed():
        pass

    @staticmethod
    def onWsError():
        pass

    @staticmethod
    def onWsConnected():
        pass
