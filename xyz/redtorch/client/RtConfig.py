import logging
import time
from threading import Timer


class RtConfig:
    # 以下配置需要手动填写
    username = None
    password = None
    operatorId = None
    authToken = None

    rpcUri = None
    websocketUri = None
    loginUri = None

    defaultRpcTimeOut = 30

    @staticmethod
    def autoConnectAndUpdateTask(interval):
        try:
            from xyz.redtorch.client.web.socket.WebSocketClientHandler import WebSocketClientHandler
            from xyz.redtorch.client.web.http.HttpClient import HttpClient
            if not WebSocketClientHandler.connected and not WebSocketClientHandler.connecting:
                loginResult = HttpClient.login(RtConfig.username, RtConfig.password)
                if loginResult:
                    operatorId = loginResult['voData']['operatorId']
                    authToken = loginResult['voData']['randomAuthToken']
                    logging.warning("登录成功,操作者ID:%s", operatorId)
                    RtConfig.operatorId = operatorId
                    RtConfig.authToken = authToken
                    WebSocketClientHandler.connect()

                    time.sleep(2)

                    from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService

                    logging.info("获取账户列表")
                    accountList = RpcClientApiService.getAccountList(sync=True)
                    logging.info("获取到%s条账户数据", len(accountList))

                    logging.info("获取持仓列表")
                    positionList = RpcClientApiService.getPositionList(sync=True)
                    logging.info("获取到%s条持仓数据", len(positionList))

                    logging.info("获取混合合约列表")
                    ContractList = RpcClientApiService.getContractList(sync=True)
                    logging.info("获取到%s条合约数据", len(ContractList))

                    logging.info("获取委托列表")
                    orderList = RpcClientApiService.getOrderList(sync=True)
                    logging.info("获取到%s条委托数据", len(orderList))

                    logging.info("获取成交列表")
                    tradeList = RpcClientApiService.getTradeList(sync=True)
                    logging.info("获取到%s条成交数据", len(tradeList))

                    logging.info("获取Tick列表")
                    tickList = RpcClientApiService.getTickList(sync=True)
                    logging.info("获取到%s条Tick数据", len(tickList))
        except:
            logging.error("定时任务发生错误", exc_info=True)
        t = Timer(interval, RtConfig.autoConnectAndUpdateTask, (interval,))
        t.start()

    @staticmethod
    def initRtClient(hostAndPort, username, password):
        RtConfig.username = username
        RtConfig.password = password
        RtConfig.rpcUri = "http://" + hostAndPort + "/api/rpc"
        RtConfig.loginUri = "http://" + hostAndPort + "/api/login"
        RtConfig.websocketUri = "ws://" + hostAndPort + "/websocket"
        RtConfig.autoConnectAndUpdateTask(15)
