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

def setRoverSpeed(ls, rs):
	print "setting speed, %d %d" % (ls, rs)
	
def setServoPos(id, pos):
	print "setting servo pos, id=%d pos=%d" % (id, pos)

def handleCommand(cmd_dict):
	cmd_id = cmd_dict[rv_protocol.KEY_CMD_ID]
	print "cmd_id = ", cmd_id
	if cmd_id == rv_protocol.CMD_ID_RV_SPEED:
		[ls, rs] = cmd_dict[rv_protocol.KEY_RV_SPEED]
		setRoverSpeed(ls, rs)
	elif cmd_id == rv_protocol.CMD_ID_SERVO_POS:
		[servo_id, pos] = cmd_dict[rv_protocol.KEY_SERVO_POS]
		setServoPos(servo_id, pos)
		
def handleNewMsg(msg):
	msg_dict = rv_protocol.parseMessage(msg)
	print "msg_dict = ", msg_dict
	if msg_dict[rv_protocol.KEY_MSG_TYPE] == rv_protocol.MSG_TYPE_RAW:
		print "raw_message = ", msg_dict[rv_protocol.KEY_MSG_RAW]
	elif msg_dict[rv_protocol.KEY_MSG_TYPE] == rv_protocol.MSG_TYPE_CMD:
		handleCommand(msg_dict[rv_protocol.KEY_MSG_CMD])
	else:
		print "msg_type not supported"

def controlEventCb(event, data):
	print "event = " + str(event)
	if(event == controlserver.EVENT_SERVER_FINISHED):
		print "server finished, exiting"
		os._exit(0)
	elif event == controlserver.EVENT_NEW_MSG:
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




