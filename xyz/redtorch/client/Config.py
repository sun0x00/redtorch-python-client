class Config:
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
