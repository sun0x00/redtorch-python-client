import logging
import time

from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService
from test.StrategyDemo import StrategyDemo
from xyz.redtorch.client.strategy.StrategyEngine import StrategyEngine
from xyz.redtorch.client.web.http.HttpClient import HttpClient
from xyz.redtorch.client.Config import Config
from xyz.redtorch.client.web.socket.WebSocketClientHandler import WebSocketClientHandler

from xyz.redtorch.pb.core_enum_pb2 import MarketDataDBTypeEnum, BarCycleEnum


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel('INFO')
    LOG_FILE = 'redtorch-python-client.' + str(time.time()) + '.log'
    BASIC_FORMAT = '%(asctime)s %(levelname)s %(filename)s:[%(lineno)s] %(funcName)s %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    streamHandler = logging.StreamHandler()  # 输出到控制台的handler
    streamHandler.setFormatter(formatter)
    # streamHandler.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
    fileHandler = logging.FileHandler("../logs/"+LOG_FILE)  # 输出到文件的handler
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    # 修改配置必要信息
    # Config.host = ""
    # Config.port = 9099
    # Config.username = 'admin'
    # Config.password = ''
    # Config.baseUrl = "http://" +  Config.host + ":" + str(Config.port)

    loginResult = HttpClient.login(Config.username, Config.password, Config.baseUrl)
    if loginResult:
        operatorId = loginResult['resultVo']['voData']['operatorId']
        nodeId = loginResult['resultVo']['voData']['recentlyNodeId']
        logging.warning("登录成功,操作者ID:%s,节点ID:%s", operatorId, nodeId)
        Config.operatorId = operatorId
        Config.nodeId = nodeId
        WebSocketClientHandler.connect(loginResult['cookie'])

        time.sleep(2)

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

        startDatetime = '2020-06-15 00:00:00.000000'
        startTimestamp = int(time.mktime(time.strptime(startDatetime, "%Y-%m-%d %H:%M:%S.%f"))*1000)

        endDatetime = '2020-06-23 00:00:00.000000'
        endTimestamp = int(time.mktime(time.strptime(endDatetime, "%Y-%m-%d %H:%M:%S.%f"))*1000)
        print(startDatetime)
        print(endTimestamp)
        barList = RpcClientApiService.queryDBBarList(startTimestamp, endTimestamp, "IC2009@CFFEX@FUTURES", BarCycleEnum.B_1Min, MarketDataDBTypeEnum.MDDT_MIX, reqId=None, timeoutSeconds=None)

        print(len(barList))

        demoStrategyId = "TEST-STRATEGY-ID-000"
        strategyDemo = StrategyDemo({"strategyId": demoStrategyId})

        StrategyEngine.addStrategy(strategyDemo)
        strategyDemo.initStrategy()

        strategyDemo.startTrading()

        while True:
            time.sleep(100)
