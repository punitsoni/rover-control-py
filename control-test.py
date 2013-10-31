#!/usr/bin/python

import time
import controlserver
import sys
import os
import select
from controlserver import ControlServer

server = None
def dataCallback(key, val):
    if key == "kill":
        server.stop()
    print "key=%s, val=%s" % (key, val)

def eventCallback(event, data):
    print "event = " + str(event)
    if(event == controlserver.EVENT_SERVER_FINISHED):
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
            os._exit(0)

    print("alive")
    time.sleep(2)
