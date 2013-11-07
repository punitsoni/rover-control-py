#!/usr/bin/python

import SocketServer
import logging
import struct

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

    def handleNewMsg(self, msg):
        raise NotImplementedError("Method not implemented")

class _MyReqHandler(SocketServer.BaseRequestHandler):

    FLAG_ACK = 1
    FLAG_NACK = 2

    def respond(self, flag, msg=""):
        data = chr(flag) + msg
        self.request.sendall(data)

    def handle(self):
        s = self.request
        recv_count = 4
        data = s.recv(recv_count)
        if data == 0:
            return
        total_rx = len(data)
        lenInfo = data
        """# temp
        b = map(ord, lenInfo)
        logger.info("msg bytes = " + str(b))
        if self.server.listener is not None:
            response = self.server.listener.handleNewMsg(lenInfo)
            logger.info("response = " + str(map(ord, response)))
            s.sendall(response)
        return
        # /temp"""
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == 0:
                return
            total_rx += len(data)
            lenInfo = lenInfo + data

        recv_count = (ord(lenInfo[0]) +	(ord(lenInfo[1]) << 8) +
            (ord(lenInfo[2]) << 16) + (ord(lenInfo[3]) << 24))
        logger.info("lenInfo = %s, msg_length = %d" %
            (str(map(ord, lenInfo)), recv_count))
        if recv_count > 1024:
            logger.info("size more than 1024 not supportedmsg_length = %d"
                % recv_count)
            self.respond(self.FLAG_NACK)
            return
        data = s.recv(recv_count)
        total_rx = len(data)
        msg = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == 0:
                return            
            total_rx += len(data)
            msg = msg + data
        if self.server.listener is not None:
            self.server.listener.handleNewMsg(msg)
        else:
            b = map(ord, msg)
            logger.info("msg bytes = " + str(b))
        self.respond(self.FLAG_ACK)
        

class _MyTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True
    
    def setListner(self, listener):
        self.listener = listener

class Server:
    """Server class that listens to control commands"""
    PORT = 9999
    
    def __init__(self, listener=None, port=None):
        if port == None:
            port = self.PORT
        self.tserver = _MyTCPServer(("", port), _MyReqHandler)
        self.tserver.setListner(listener)
        
    def serveForever(self):
        self.tserver.serve_forever()
        
    def sendMsg(self, msg):
        logger.info("len = %d" % len(msg))
        data = struct.pack(">I", len(msg))
        logger.info("sending message bytes: " + str(map(ord, msg)))

if __name__ == "__main__":
    setLoglevel(logging.INFO)
    s = Server()
    print "starting server.."
    s.serveForever()

