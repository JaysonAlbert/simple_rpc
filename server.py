# -*- coding: utf-8 -*-
from rpc import *

def hello(a):
    return 2*a

if __name__ == '__main__':
    host = 'localhost'
    port = 1111
    RpcHandler.register(hello)
    server = SocketServer.TCPServer((host, port), RpcHandler)
    server.serve_forever()