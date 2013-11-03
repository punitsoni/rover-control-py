#!/usr/bin/python

# Message Format
# |length:1|msgtype:1|msgdata:(length-1)|
#
# For Commands, msgtype = 1
# |length:1|0x01|cmd_id:1|cmd_data:(length - 2)|

import logging

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
CMD_ID_MAX          = 255

KEY_MSG_TYPE = "msg-type"
KEY_MSG_RAW = "msg-raw"
KEY_MSG_CMD = "msg-cmd"
KEY_CMD_ID = "cmd-id"
KEY_RV_SPEED = "rv-speed"
KEY_SERVO_ID = "servo-id"
KEY_SERVO_POS = "servo-pos"

def parseCommand(cmd):
    cmd_id = cmd[0]
    ret = {KEY_CMD_ID:cmd_id}
    if cmd_id == CMD_ID_RV_SPEED:
        ls = cmd[1]
        rs = cmd[2]
        ret.update({KEY_RV_SPEED:[ls, rs]})
    elif cmd_id == CMD_ID_SERVO_POS:
        servo_id = cmd[1]
        pos = cmd[2]
        ret.update({KEY_SERVO_ID:servo_id, KEY_SERVO_POS:pos})
    else:
        logger.error("invalid cmd id")
        return None
    return ret

def parseMessage(msg):
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

# test code
if __name__ == '__main__':
    testMsg1 = [0, "Hello"]
    print "testMsg1 = ", parseMessage(testMsg1)

    testMsg2 = [1, 0, 60, 40]
    print "testMsg2 = ", parseMessage(testMsg2)


