import json
import logging

import requests

from xyz.redtorch.client.RtConfig import RtConfig

logger = logging.getLogger('HttpClient')


class HttpClient:
    @staticmethod
    def login(username, password):
        try:
            payload = {
                'username': username,
                'password': password
            }
            headers = {'content-type': 'application/json'}
            loginRet = requests.post(RtConfig.loginUri, data=json.dumps(payload), headers=headers)
            if loginRet.status_code == 200:
                loginResult = loginRet.json()
                if loginResult['status']:
                    logger.info("登录成功")
                    return loginResult
                else:
                    logger.error("服务器返回登录失败")
                    return None
            else:
                logger.error("服务器返回非200状态码")
                return None
        except:
            logger.error("登录发生异常", exc_info=True)
            return None
