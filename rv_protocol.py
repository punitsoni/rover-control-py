#!/usr/bin/python

# Message Format
# |length:1|msgtype:1|msgdata:(length-1)|
#
# For Commands, msgtype = 1
# |length:1|0x01|cmd_id:1|cmd_data:(length - 2)|

import logging
import struct

# setup logging for module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#messages
MSG_TYPE_RAW        = 0
MSG_TYPE_CMD        = 1
MSG_TYPE_STATUS     = 2
MSG_TYPE_MAX        = 255

#commands
CMD_ID_RV_SPEED     = 0
CMD_ID_SERVO_POS    = 1
CMD_ID_RESET        = 2
CMD_ID_GET_STATUS   = 3
CMD_ID_MAX          = 255

#response
RESP_ACK = 10
RESP_NACK = 11

#status
STATUS_ID_RV_SPEED = 0
STATUS_ID_SERVO_POS = 1

KEY_MSG_TYPE = "msg-type"
KEY_MSG_TIMESTAMP = "msg_timestamp"
KEY_MSG_RAW = "msg-raw"
KEY_MSG_CMD = "msg-cmd"
KEY_CMD_ID = "cmd-id"
KEY_RV_SPEED = "rv-speed"
KEY_SERVO_POS = "servo-pos"

def parseCommand_old(cmd):
    cmd_id = cmd[0]
    ret = {KEY_CMD_ID:cmd_id}
    if cmd_id == CMD_ID_RV_SPEED:
        ls = cmd[1]
        rs = cmd[2]
        ret.update({KEY_RV_SPEED:[ls, rs]})
    elif cmd_id == CMD_ID_SERVO_POS:
        servo_id = cmd[1]
        pos = cmd[2]
        ret.update({KEY_SERVO_POS:[servo_id, pos]})
    else:
        logger.error("invalid cmd id")
        return None
    return ret

def createStatusMsg(s):
    msg = struct.pack(">B", MSG_TYPE_STATUS)
    if KEY_RV_SPEED in s:
        [ls, rs] = s[KEY_RV_SPEED]
        msg += struct.pack(">B", STATUS_ID_RV_SPEED)
        msg += struct.pack(">b", ls)
        msg += struct.pack(">b", rs)
    if KEY_SERVO_POS in s:
        [sid, pos] = s[KEY_SERVO_POS]
        msg += struct.pack(">B", STATUS_ID_SERVO_POS)
        msg += struct.pack(">B", sid)
        msg += struct.pack(">B", pos)
    return msg

def parseCommand(cmd):
    cmd_id = struct.unpack("!B", cmd[0])[0]
    ret = {KEY_CMD_ID:cmd_id}
    if cmd_id == CMD_ID_RV_SPEED:
        ls = struct.unpack("!b", cmd[1])[0]
        rs = struct.unpack("!b", cmd[2])[0]
        ret.update({KEY_RV_SPEED:[ls, rs]})
    elif cmd_id == CMD_ID_SERVO_POS:
        servo_id = struct.unpack("!B", cmd[1])[0]
        pos = struct.unpack("!B", cmd[2])[0]
        ret.update({KEY_SERVO_POS:[servo_id, pos]})
    else:
        logger.error("invalid cmd id")
        return None
    return ret

def parseMessage_old(msg):
    msgtype = msg[0]
    ret = {KEY_MSG_TYPE:msgtype}
    if msgtype == MSG_TYPE_RAW:
        rawdata = msg[1:]
        ret.update({KEY_MSG_RAW:rawdata})
    elif msgtype == MSG_TYPE_CMD:
        cmd_dict = parseCommand(msg[1:])
        if cmd_dict == None:
            logger.error("parseCommand failed")
            return None
        ret.update({KEY_MSG_CMD:cmd_dict})
    else:
        logger.error("invalid msg type")
        return None
    return ret

def parseMessage(msg):
    msgtype = struct.unpack("!B", msg[0])[0]
    ret = {KEY_MSG_TYPE:msgtype}
    if msgtype == MSG_TYPE_RAW:
        rawdata = msg[1:]
        ret.update({KEY_MSG_RAW:rawdata})
    elif msgtype == MSG_TYPE_CMD:
        cmd_dict = parseCommand(msg[1:])
        if cmd_dict == None:
            logger.error("parseCommand failed")
            return None
        ret.update({KEY_MSG_CMD:cmd_dict})
    else:
        logger.error("invalid msg type")
        return None
    return ret

# test code
if __name__ == '__main__':
    testMsg1 = [0, "Hello"]
    print "testMsg1 = ", parseMessage(testMsg1)

    testMsg2 = [1, 0, 60, 40]
    print "testMsg2 = ", parseMessage(testMsg2)


