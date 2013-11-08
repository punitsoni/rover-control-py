#!/usr/bin/env python

import select
import socket
import sys
import threading
import os
import time
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

EVENT_SERVER_FINISHED = 0
EVENT_SERVER_TIMEDOUT = 1
EVENT_NEW_MSG = 2


class ControlServer():
    'Listens to control commands from clients'
    maxClients = 1
    SOCK_HOST = ''
    SOCK_PORT = 50000
    DATA_PACKET_SIZE = 1024

    def __init__(self):
        self.host = ControlServer.SOCK_HOST
        self.port = ControlServer.SOCK_PORT
        self.size = ControlServer.DATA_PACKET_SIZE
        self.server = None
        self.numClients = 0
        self.client = None
        self.clientAddr = None
        self.cLock = threading.Lock()
        self.eventCb = None

    def openSocket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            logger.error("Could not open socket: " + message)
            sys.exit(1)


    def start(self, eventCb):
        logger.info("starting server thread")
        self.eventCb = eventCb
        t = threading.Thread(target=self.run)
        t.start()

    def sendDataToClient(self, data=None):
        if self.numClients < 1:
            self.logging.error("no clients alive")
            return
        self.cLock.acquire(True)
        self.client.send(data)
        self.cLock.release()

    def stop(self):
        logger.info("stopping server")
        self.running = False

    def sendEventCb(self, event, data):
        if self.eventCb:
            self.eventCb(event, data)

    def decodeFrameLen(self, lenInfo):
        len = (ord(lenInfo[0]) + (ord(lenInfo[1]) << 8) +
            (ord(lenInfo[2]) << 16) + (ord(lenInfo[3]) << 24))
        return len

    def recvFrameMessage(self, s):
        recv_count = 4;
        data = s.recv(recv_count)#.decode("ascii")
        if data == 0:
            return None
        total_rx = len(data)
        lenInfo = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == 0:
                return None
            total_rx += len(data)
            lenInfo = lenInfo + data

        recv_count = self.decodeFrameLen(lenInfo)
        logger.info("length = %d" % recv_count)

        data = s.recv(recv_count)
        total_rx = len(data)
        msg = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx)
            if data == 0:
                return None
            total_rx += len(data)
            msg = msg + data
        #msg = map(ord, msg)
        #logger.debug("msg = " + str(msg))
        return msg

    def run(self):
        self.openSocket()
        input = [self.server]
        self.running = True
        while self.running:
            if(self.numClients == 0):
                logger.info("waiting for a client to connect...")
            inputready,outputready,exceptready = select.select(input,[],[])
            for s in inputready:
                if s == self.server:
                    client, addr = self.server.accept()
                    if(self.numClients >= self.maxClients):
                        client.send('max limit reached. maxClients='
                                + str(self.maxClients))
                        client.close()
                    logger.info("connected to new client " + str(addr))
                    input.append(client)
                    self.numClients += 1
                    self.client = client
                    self.sendDataToClient("cmd>")
                else:
                    msg = self.recvFrameMessage(s)
                    if msg:
                        self.sendEventCb(EVENT_NEW_MSG, msg)
                    else:
                        s.close()
                        input.remove(s)
                        logger.info("client removed")
                        self.numClients -= 1
        self.server.close()
        logger.info("server finished")
        self.sendEventCb(EVENT_SERVER_FINISHED)

## Module testing code ##
if __name__ == "__main__":
    print "Press Enter to Exit"
    server = None
    def eventCallback(event, data):
        print "event = " + str(event)
        if(event == EVENT_SERVER_FINISHED):
            print "server finished, exiting"
            os._exit(0)
    	elif event == EVENT_NEW_MSG:
    		print "new_msg = ", data

    server = ControlServer()
    setLoglevel(logging.INFO)
    server.start(eventCallback)
    while True:
        input = [sys.stdin]
        inputready,outputready,exceptready = select.select(input,[],[])
        for s in inputready:
            if s == sys.stdin:
                junk = sys.stdin.readline()
                print "BYE"
                os._exit(0)
