import logging
import time

from xyz.redtorch.client.service.rpc.RpcClientApiService import RpcClientApiService
from test.StrategyDemo import StrategyDemo
from xyz.redtorch.client.strategy.StrategyEngine import StrategyEngine
from xyz.redtorch.client.web.http.HttpClient import HttpClient
from xyz.redtorch.client.RtConfig import RtConfig
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
    # RtConfig.host = ""
    # RtConfig.port = 9099
    # RtConfig.username = 'admin'
    # RtConfig.password = ''

    RtConfig.initRtClient()

    while not WebSocketClientHandler.connected:
        time.sleep(5)

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
