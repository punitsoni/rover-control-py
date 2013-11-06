#!/usr/bin/python

import SocketServer
import logging

# setup logging for module
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def setLoglevel(level):
    logger.setLevel(level)

class MsgListener:
    """Abstract Listner class for control messages."""
    def handleNewMsg(self):
        raise NotImplementedError("Method not implemented")

class _MyReqHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        s = self.request
        recv_count = 4
        data = s.recv(recv_count)
        if data == 0:
            return None
        total_rx = len(data)
        lenInfo = data
        #msg = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == 0:
                return None
            total_rx += len(data)
            lenInfo = lenInfo + data

        recv_count = (ord(lenInfo[0]) +	(ord(lenInfo[1]) << 8) +
            (ord(lenInfo[2]) << 16) + (ord(lenInfo[3]) << 24))
        logger.info("msg_length = %d" % recv_count)
        
        data = s.recv(recv_count)
        total_rx = len(data)
        msg = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == 0:
                return None            
            total_rx += len(data)
            msg = msg + data
        if self.server.listener is not None:
            self.server.listener.handleNewMsg(msg)
        else:
            bytes = map(ord, msg)
            logger.info("msg bytes = " + str(bytes))
        

class _MyTCPServer(SocketServer.TCPServer):
    def setListner(self, listener):
        self.listener = listener

class Server:
    """Server class that listens to control commands"""
    HOST, PORT = "", 9999
    def __init__(self, listener=None):
        self.tserver = _MyTCPServer((self.HOST, self.PORT), _MyReqHandler)
        self.tserver.setListner(listener)
    def serveForever(self):
        self.tserver.serve_forever()

if __name__ == "__main__":
    setLoglevel(logging.INFO)
    s = Server()
    print "starting server.."
    s.serveForever()

