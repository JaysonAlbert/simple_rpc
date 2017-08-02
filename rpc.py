# -*- coding: utf-8 -*-

import zlib
import socket
import struct
import SocketServer
import threading
import cPickle

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = zlib.compress(cPickle.dumps(msg), 3)
    length = len(msg)
    msg = struct.pack('>I', length) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = sock.recv(4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return cPickle.loads(zlib.decompress(data))

class RpcHandler(SocketServer.StreamRequestHandler):

    __functions = {}

    def handle(self):
        while self.request:
            data = recv_msg(self.request)
            if not data:
                break
            name, args, kwargs = data
            func = RpcHandler.__functions[name]
            rt = func(*args, **kwargs)
            send_msg(self.request,rt)

    @staticmethod
    def register(func):
        RpcHandler.__functions[func.__name__] = func
