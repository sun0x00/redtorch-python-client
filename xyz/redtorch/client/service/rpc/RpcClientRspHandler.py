import logging as logger
from threading import RLock


class RpcClientRspHandler:
    __waitTransactionIdSet = set()
    __waitTransactionIdSetLock = RLock()
    __rpcRspDict = dict()

    @staticmethod
    def registerTransactionId(transactionId):
        cls = RpcClientRspHandler
        cls.__waitTransactionIdSetLock.acquire()
        try:
            cls.__waitTransactionIdSet.add(transactionId)
        finally:
            cls.__waitTransactionIdSetLock.release()

    @staticmethod
    def unregisterTransactionId(transactionId):
        cls = RpcClientRspHandler
        cls.__waitTransactionIdSetLock.acquire()
        try:
            if transactionId in cls.__waitTransactionIdSet:
                cls.__waitTransactionIdSet.remove(transactionId)
        finally:
            cls.__waitTransactionIdSetLock.release()

    @staticmethod
    def containsTransactionId(transactionId):
        cls = RpcClientRspHandler
        cls.__waitTransactionIdSetLock.acquire()
        try:
            if transactionId in cls.__waitTransactionIdSet:
                return True
        finally:
            cls.__waitTransactionIdSetLock.release()

        return False

    @staticmethod
    def getAndRemoveRpcRsp(transactionId):

        cls = RpcClientRspHandler

        cls.__waitTransactionIdSetLock.acquire()
        try:
            if transactionId in cls.__rpcRspDict:
                cls.__waitTransactionIdSet.remove(transactionId)
                return cls.__rpcRspDict.pop(transactionId)
            else:
                return None
        finally:
            cls.__waitTransactionIdSetLock.release()

    @staticmethod
    def onRpcRsp(transactionId, rsp):
        cls = RpcClientRspHandler

        cls.__waitTransactionIdSetLock.acquire()
        try:
            if transactionId in cls.__waitTransactionIdSet:
                cls.__rpcRspDict[transactionId] = rsp
            else:
                logger.info("直接丢弃的回报,业务ID:%s", transactionId)
        finally:
            cls.__waitTransactionIdSetLock.release()
