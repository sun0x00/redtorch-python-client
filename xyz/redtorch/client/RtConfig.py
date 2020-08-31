import logging
import time
from threading import Timer

from xyz.redtorch.client.web.http.HttpClient import HttpClient


class RtConfig:
    # 以下配置需要手动填写
    host = "127.0.0.1"
    port = 9099
    username = 'admin'
    password = 'rt-admin'
    baseUrl = "http://" + host + ":" + str(port)

    rpcTimeOut = 10

    # 以下配置自动获取
    operatorId = None
    nodeId = None

    @staticmethod
    def autoConnectAndUpdateTask(interval):
        try:

            from xyz.redtorch.client.web.socket.WebSocketClientHandler import WebSocketClientHandler
            if not WebSocketClientHandler.connected and not WebSocketClientHandler.connecting:
                loginResult = HttpClient.login(RtConfig.username, RtConfig.password, RtConfig.baseUrl)
                if loginResult:
                    operatorId = loginResult['resultVo']['voData']['operatorId']
                    nodeId = loginResult['resultVo']['voData']['recentlyNodeId']
                    logging.warning("登录成功,操作者ID:%s,节点ID:%s", operatorId, nodeId)
                    RtConfig.operatorId = operatorId
                    RtConfig.nodeId = nodeId
                    WebSocketClientHandler.connect(loginResult['cookie'])

                    time.sleep(2)

                    from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService

                    logging.info("获取账户列表")
                    RpcClientApiService.getAccountList(sync=True)
                    logging.info("获取持仓列表")
                    RpcClientApiService.getPositionList(sync=True)
                    logging.info("获取混合合约列表")
                    RpcClientApiService.getMixContractList(sync=True)
                    logging.info("获取委托列表")
                    RpcClientApiService.getOrderList(sync=True)
                    logging.info("获取成交列表")
                    RpcClientApiService.getTradeList(sync=True)
                    logging.info("获取Tick列表")
                    RpcClientApiService.getTickList(sync=True)
        except:
            logging.error("定时更新最新净值发生错误", exc_info=True)
        t = Timer(interval, RtConfig.autoConnectAndUpdateTask, (interval,))
        t.start()

    @staticmethod
    def initRtClient():

        RtConfig.baseUrl = "http://" + RtConfig.host + ":" + str(RtConfig.port)
        RtConfig.autoConnectAndUpdateTask(15)
