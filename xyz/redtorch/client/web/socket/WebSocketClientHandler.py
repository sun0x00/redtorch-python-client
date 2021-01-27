import asyncio
import json
import logging as logger

import websockets

from xyz.redtorch.client.RtConfig import RtConfig

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
    async def connectAsyncWS():

        try:
            async with websockets.connect(
                    RtConfig.websocketUri, max_size=1_000_000_000_000
            ) as websocket:

                WebSocketClientHandler._ws = websocket

                from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
                RpcClientProcessService.onWsConnected()
                logger.info("连接已建立,发送认证")

                await websocket.send(json.dumps({"Auth-Token": RtConfig.authToken}))

                async for message in websocket:
                    if isinstance(message, bytes):
                        from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
                        RpcClientProcessService.processData(message)
                    else:
                        if WebSocketClientHandler.connecting:
                            data = json.loads(message)
                            if data['verified']:
                                logger.info("验证通过")
                                WebSocketClientHandler.connecting = False
                                WebSocketClientHandler.connected = True
                            else:
                                logger.info("验证失败")

        except:
            logger.error("WebSocket连接断开", exc_info=True)
        finally:
            from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
            RpcClientProcessService.onWsClosed()
            WebSocketClientHandler._ws = None
            WebSocketClientHandler.connecting = False
            WebSocketClientHandler.connected = False

    @staticmethod
    def connect():

        if WebSocketClientHandler._ws is None and not WebSocketClientHandler.connecting:
            WebSocketClientHandler.connecting = True
            try:
                if WebSocketClientHandler.eventLoop is not None:
                    try:
                        WebSocketClientHandler.eventLoop.close()
                    except:
                        logger.error("关闭过期事件循环发生错误", exc_info=True)
                    WebSocketClientHandler.eventLoop = None

                WebSocketClientHandler.eventLoop = asyncio.new_event_loop()
                asyncio.set_event_loop(WebSocketClientHandler.eventLoop)
                thread.start_new_thread(asyncio.get_event_loop().run_until_complete,
                                        (WebSocketClientHandler.connectAsyncWS(),))
                logger.info("创建WebSocket线程")
            except:
                logger.error("创建会话实例异常", exc_info=True)
                WebSocketClientHandler.connecting = False
        else:
            logger.info("会话实例已存在或正在创建,不可重复创建")

    @staticmethod
    def sendData(data):
        if not WebSocketClientHandler._ws:
            logger.error("发送二进制数据错误，连接不存在或已经断开")
            return False

        try:
            asyncio.run_coroutine_threadsafe(WebSocketClientHandler._ws.send(data),
                                             WebSocketClientHandler.eventLoop).result()
        except:
            logger.error("发送二进制数据错误", exc_info=True)
            return False

        return True
