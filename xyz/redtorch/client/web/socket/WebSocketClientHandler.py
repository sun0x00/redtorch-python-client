import logging as logger

from xyz.redtorch.client.RtConfig import RtConfig
import asyncio
import websockets

try:
    import thread
except ImportError:
    import _thread as thread


class WebSocketClientHandler:
    _ws = None

    connected = False
    connecting = False
    eventLoop = None

    @staticmethod
    async def connectAsyncWS(headers):

        try:
            wsUri = "ws://" + RtConfig.host + ":" + str(RtConfig.port) + "/websocket"
            async with websockets.connect(
                    wsUri, extra_headers=headers, max_size=1_000_000_000_000
            ) as websocket:

                WebSocketClientHandler._ws = websocket
                WebSocketClientHandler.connecting = False
                WebSocketClientHandler.connected = True

                from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
                RpcClientProcessService.onWsConnected()
                logger.info("连接已建立")

                async for message in websocket:
                    if isinstance(message, bytes):
                        from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
                        RpcClientProcessService.processData(message)
                    else:
                        logger.warning("接收到非二进制消息")

        except Exception as e:
            logger.error("WebSocket连接断开", e)
        finally:
            from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
            RpcClientProcessService.onWsClosed()
            WebSocketClientHandler._ws = None
            WebSocketClientHandler.connecting = False
            WebSocketClientHandler.connected = False

    @staticmethod
    def connect(cookie):

        if WebSocketClientHandler._ws is None and not WebSocketClientHandler.connecting:
            WebSocketClientHandler.connecting = True
            try:
                WebSocketClientHandler.eventLoop = asyncio.new_event_loop()
                asyncio.set_event_loop(WebSocketClientHandler.eventLoop)
                thread.start_new_thread(asyncio.get_event_loop().run_until_complete,
                                        (WebSocketClientHandler.connectAsyncWS({'cookie': cookie}),))
                logger.info("创建WebSocket线程")
            except Exception as e:
                logger.error("创建会话实例异常")
                logger.error(e, exc_info=True)
                WebSocketClientHandler.connecting = False
        else:
            logger.info("会话实例已存在或正在创建,不可重复创建")

    @staticmethod
    def sendData(data):
        if not WebSocketClientHandler._ws:
            logger.error("发送二进制数据错误，连接不存在或已经断开")
            return False

        try:
            asyncio.run_coroutine_threadsafe(WebSocketClientHandler._ws.send(data), WebSocketClientHandler.eventLoop).result()
        except Exception as e:
            logger.error("发送二进制数据错误")
            logger.error(e, exc_info=True)
            return False

        return True
