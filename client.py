# -*- coding: utf-8 -*-
from rpc import *
import time

class RpcClient(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        errno = self.sock.connect_ex((address, port))
        if errno != 0:
            print("connectting to server failed")

    def __getattr__(self, name):
        """实现远程调用功能"""

        # 执行远程调用任务
        def dorpc(*args, **kwargs):
            # 生成请求
            req = [name, args, kwargs]

            send_msg(self.sock, req)
            repb = recv_msg(self.sock)
            return repb

        return dorpc

if __name__ == '__main__':
    host = 'localhost'
    port = 1111

    client = RpcClient(host,port)
    print(client.hello(4))
    client = RpcClient(host, port)
    print(client.hello('12345'))
