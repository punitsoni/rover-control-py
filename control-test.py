#!/usr/bin/python

import time
from controlserver import ControlServer

server = None

def dataCallback(data):
    print "callback: data=" + data
    if data == "kill":
        server.stop()
    temp = data.split()
    print "key=%s, val=%s" % (temp[0], temp[1])

server = ControlServer()
server.start(dataCallback)
while True:
    print("alive")
    time.sleep(2)
