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
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(name)s:%(message)s')
ch.setFormatter(formatter)

def setLogLevel(level):
    logger.setLevel(level)

EVENT_SERVER_FINISHED = 0
EVENT_SERVER_TIMEDOUT = 1

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
        self.dataCb = None

    def openSocket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            logger.error("Could not open socket: " + message)
            sys.exit(1)


    def start(self, dataCb, eventCb):
        logger.info("starting server thread")
        self.dataCb = dataCb
        self.eventCb = eventCb
        t = threading.Thread(target=self.run)
#        t.daemon = True
        t.start()

    def sendDataToClient(self, data):
        if self.numClients < 1:
            self.logging.error("no clients alive")
            return
        self.cLock.acquire(True)
        self.client.send(data)
        self.cLock.release()

    def stop(self):
        logger.info("stopping server")
        self.running = False

    def sendEvent(self, event):
        if self.eventCb:
            self.eventCb(event, None)

    def decodeFrameLen(self, lenInfo):
        len = (ord(lenInfo[0]) + (ord(lenInfo[1]) << 8) +
            (ord(lenInfo[2]) << 16) + (ord(lenInfo[3]) << 24))
        return len

    def recvFrameMessage(self, s):
        recv_count = 4;
        data = s.recv(recv_count).decode("ascii")
        if !data:
            return None
        total_rx = len(data)
        lenInfo = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx).decode("ascii")
            if !data:
                return None
            total_rx += len(data)
            lenInfo = lenInfo + data

        recv_count = self.decodeFrameLen(lenInfo)
        logger.info("length = %d" % recv_count)
        
        data = s.recv(recv_count).decode("ascii")
        total_rx = len(data)
        msg = data
        while total_rx < recv_count:
            data = s.recv(recv_count - total_rx).decode("ascii")
            if !data:
                return None            
            total_rx += len(data)
            msg = msg + data
        logger.info("msg = " + msg)
        
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
                    #data = s.recv(self.size)
                    #if data:
                    #    self.processClientData(data)
                    #else:
                    #    s.close()
                    #    input.remove(s)
                    #    logger.info("client removed")
                    #    self.numClients -= 1
        self.server.close()
        logger.info("server finished")
        self.sendEvent(EVENT_SERVER_FINISHED)

## Module testing code ##
if __name__ == "__main__":
    print "Press Enter to Exit"
    server = None
    def dataCallback(key, val):
        if key == "kill":
            server.stop()
        print "key=%s, val=%s" % (key, val)

    def eventCallback(event, data):
        print "event = " + str(event)
        if(event == EVENT_SERVER_FINISHED):
            print "server finished, exiting"
            os._exit(0)

    server = ControlServer()
    server.start(dataCallback, eventCallback)
    while True:
        input = [sys.stdin]
        inputready,outputready,exceptready = select.select(input,[],[])
        for s in inputready:
            if s == sys.stdin:
                junk = sys.stdin.readline()
                print "BYE"
                os._exit(0)
