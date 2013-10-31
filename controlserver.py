#!/usr/bin/env python

import select
import socket
import sys
import threading
import os
import time
import logging

class ControlServer(threading.Thread):
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
        self.setUpLogging()
        self.cLock = threading.Lock()

    def setUpLogging(self):
        logger = logging.getLogger('ControlServer')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(name)s:%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.logger = logger


    def openSocket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            self.logger.error("Could not open socket: " + message)
            sys.exit(1)

    def setLogLevel(self, level):
        self.logger.setLevel(level)

    def start(self, dataCb):
        self.logger.info("starting server thread")
        self.dataCb = dataCb
        t = threading.Thread(target=self.run)
        t.start()

    def sendDataToClient(self, data):
        if self.numClients < 1:
            self.logging.error("no clients alive")
            return
        self.cLock.acquire(True)
        self.client.send(data)
        self.cLock.release()

    def stop(self):
        self.logger.info("stopping server")
        self.running = False

    def processClientData(self, data):
        s = data.strip()
        temp = data.split()
        if len(temp) != 2:
            self.logger.warning("invalid data: " +  data)
            self.sendDataToClient("NACK")
            return
        self.dataCb(temp[0], temp[1])
        self.sendDataToClient("ACK")
        self.sendDataToClient("cmd>")
        

    def run(self):
        self.openSocket()
        input = [self.server]
        self.running = True
        while self.running:
            if(self.numClients == 0):
                self.logger.info("waiting for a client to connect...")
            inputready,outputready,exceptready = select.select(input,[],[])
            for s in inputready:
                if s == self.server:
                    client, addr = self.server.accept()
                    if(self.numClients >= self.maxClients):
                        client.send('max limit reached. maxClients='
                                + str(self.maxClients))
                        client.close()
                    self.logger.info("connected to new client " + str(addr))
                    input.append(client)
                    self.numClients += 1
                    self.client = client
                    self.sendDataToClient("cmd>")
                else:
                    data = s.recv(self.size)
                    if data:
                        self.processClientData(data)
                    else:
                        s.close()
                        input.remove(s)
                        self.logger.info("client removed")
                        self.numClients -= 1
        self.server.close()
        self.logger.info("server finished")

server = None
def dataCallback(key, val):

    if key == "kill":
        server.stop()
    print "key=%s, val=%s" % (key, val)

if __name__ == "__main__":
    server = ControlServer()
    #server.setLogLevel(logging.INFO)
    server.start(dataCallback)
    while True:
        print("alive")
        time.sleep(2)
