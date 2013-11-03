#!/usr/bin/python

import logging
import controlserver
import rv_protocol
import sys
import select
import os

# setup logging for module
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def handleNewMsg(msg):
	msg_dict = rv_protocol.parseMessage(msg)
	print "msg = ", msg_dict 

def controlEventCb(event, data):
	print "event = " + str(event)
	if(event == controlserver.EVENT_SERVER_FINISHED):
		print "server finished, exiting"
		os._exit(0)
	elif event == controlserver.EVENT_NEW_MSG:
		print "new_msg = ", data
		handleNewMsg(data)

# main #
controlserver.setLoglevel(logging.INFO)
server = controlserver.ControlServer()
server.start(controlEventCb)

while True:
        input = [sys.stdin]
        inputready,outputready,exceptready = select.select(input,[],[])
        for s in inputready:
            if s == sys.stdin:
                junk = sys.stdin.readline()
                print "BYE"
                os._exit(0)




