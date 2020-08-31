import requests
import json
import logging

logger = logging.getLogger('HttpClient')


class HttpClient:
    @staticmethod
    def login(username, password, baseUrl):
        try:
            payload = {
                'username': username,
                'password': password
            }
            headers = {'content-type': 'application/json'}
            loginRet = requests.post(baseUrl + "/api/login", data=json.dumps(payload), headers=headers)
            if loginRet.status_code == 200:
                loginResult = loginRet.json()
                cookie = loginRet.headers['Set-Cookie']
                if loginResult['status']:
                    logger.info("登录成功")
                    return {
                        "cookie": cookie,
                        "resultVo": loginResult
                    }
                else:
                    logger.error("服务器返回登录失败")
                    return None
            else:
                logger.error("服务器返回非200状态码")
                return None
        except:
            logger.error("登录发生异常", exc_info=True)
            return None
