import logging as logger

from xyz.redtorch.client.Config import Config
import websocket

try:
    import thread
except ImportError:
    import _thread as thread


class WebSocketClientHandler:
    # _instance = None
    # @staticmethod
    # def getInstance():
    #     cls = __class__
    #
    #     if cls._instance is None:
    #         cls._instance = super(cls, cls).__new__(cls)
    #     return cls._instance

    _ws = None

    @staticmethod
    def onMessage(ws, message):
        if isinstance(message, bytes):
            from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
            RpcClientProcessService.processData(message)
        else:
            logger.warning("接收到非二进制消息")

    @staticmethod
    def onError(ws, e):
        logger.error("传输错误")
        logger.error(e, exc_info=True)
        from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
        RpcClientProcessService.onWsError()
        try:
            ws.colse()
        except Exception as e:
            logger.error("传输错误后尝试关闭发生错误")
            logger.error(e, exc_info=True)

    @staticmethod
    def onClose(ws):
        from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
        RpcClientProcessService.onWsClosed()
        WebSocketClientHandler._ws = None
        logger.error("会话关闭")

    @staticmethod
    def onOpen(ws):
        from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
        RpcClientProcessService.onWsConnected()
        logger.info("连接已建立")

    @staticmethod
    def connect(cookie):
        if not WebSocketClientHandler._ws:
            try:
                wsUri = "ws://" + Config.host + ":" + str(Config.port) + "/websocket"
                ws = websocket.WebSocketApp(wsUri, cookie=cookie,
                                            on_message=WebSocketClientHandler.onMessage,
                                            on_error=WebSocketClientHandler.onError,
                                            on_close=WebSocketClientHandler.onClose)
                ws.on_open = WebSocketClientHandler.onOpen
                thread.start_new_thread(ws.run_forever, ())
                WebSocketClientHandler._ws = ws

                logger.info("创建会话实例")
            except Exception as e:
                logger.error("创建会话实例异常")
                logger.error(e, exc_info=True)
        else:
            logger.info("会话实例已存在,不可创建")

    @staticmethod
    def sendData(data):
        if not WebSocketClientHandler._ws:
            logger.error("发送二进制数据错误，连接不存在或已经断开")
            return False

        try:
            WebSocketClientHandler._ws.send(data, opcode=0x2)
        except Exception as e:
            logger.error("发送二进制数据错误")
            logger.error(e, exc_info=True)
            return False

        return True
