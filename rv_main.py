#!/usr/bin/python

import logging
import ControlServer
import rv_protocol

# setup logging for module
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class RvController(ControlServer.MsgListener):

    def __init__(self):
        self.server = ControlServer.Server(self)
        self.lspeed = 0
        self.rspeed = 0
        self.pos = 0
    
    def run(self):
        self.server.serveForever()
    
    def setRoverSpeed(self, ls, rs):
        print "setting speed, %d %d" % (ls, rs)
        self.lspeed = ls
        self.rspeed = rs
        
    def setServoPos(self, id, pos):
        print "setting servo pos, id=%d pos=%d" % (id, pos)
        self.pos = pos

    def handleCommand(self, cmd_dict):
        cmd_id = cmd_dict[rv_protocol.KEY_CMD_ID]
        print "cmd_id = ", cmd_id
        if cmd_id == rv_protocol.CMD_ID_RV_SPEED:
            [ls, rs] = cmd_dict[rv_protocol.KEY_RV_SPEED]
            self.setRoverSpeed(ls, rs)
        elif cmd_id == rv_protocol.CMD_ID_SERVO_POS:
            [servo_id, pos] = cmd_dict[rv_protocol.KEY_SERVO_POS]
            self.setServoPos(servo_id, pos)
            
    def handleNewMsg(self, msg):
        msg_dict = rv_protocol.parseMessage(msg)
        print "msg_dict = ", msg_dict
        if msg_dict is None:
            return self.sendStatus()
        if msg_dict[rv_protocol.KEY_MSG_TYPE] == rv_protocol.MSG_TYPE_RAW:
            print "raw_message = ", msg_dict[rv_protocol.KEY_MSG_RAW]
        elif msg_dict[rv_protocol.KEY_MSG_TYPE] == rv_protocol.MSG_TYPE_CMD:
            self.handleCommand(msg_dict[rv_protocol.KEY_MSG_CMD])
        else:
            print "msg_type not supported"
            
    def sendStatus(self):
        status = {rv_protocol.KEY_RV_SPEED:[self.lspeed, self.rspeed]}
        status.update({rv_protocol.KEY_SERVO_POS:[12, self.pos]})
        msg = rv_protocol.createStatusMsg(status)
        return msg
        #self.server.sendMsg(msg)
    

# main #
ControlServer.setLoglevel(logging.INFO)
controller = RvController()

print "starting controller"

controller.run()


