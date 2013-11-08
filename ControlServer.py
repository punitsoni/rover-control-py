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

    def _recvNBytes(self, s, n):
        recv_count = n
        data = s.recv(recv_count)
        if data == None or len(data) == 0:
            return None
        total_rx = len(data)
        final_data = data

        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == None or len(data) == 0:
                return None
            total_rx += len(data)
            final_data += data
        return final_data

    # handles one client connection
    def handle(self):
        s = self.request
        connected = True
        # run while client is connected
        while True:
            lenInfo = self._recvNBytes(s, 4)
            if lenInfo == None:
                break

            msglen = (ord(lenInfo[0]) +	(ord(lenInfo[1]) << 8) +
                (ord(lenInfo[2]) << 16) + (ord(lenInfo[3]) << 24))
            logger.info("lenInfo = %s, msg_length = %d" %
                (str(map(ord, lenInfo)), msglen))

            if msglen > 1024:
                logger.info("size more than 1024 not supportedmsg_length = %d"
                    % msglen)
                self.respond(self.FLAG_NACK)
                return None

            msg = self._recvNBytes(s, msglen)
            if msg == None:
                break

            logger.info("msg bytes = " + str(map(ord, msg)))
            if self.server.listener is not None:
                self.server.listener.handleNewMsg(msg)
            self.respond(self.FLAG_ACK)
        logger.info("Client disconnected.")


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

if __name__ == "__main__":
    setLoglevel(logging.INFO)
    s = Server()
    print "starting server.."
    s.serveForever()

