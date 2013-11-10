#!/usr/bin/python

import logging
import smbus
import time

# setup logging for module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

curRoverSpeed = [0, 0]
curCamPos = [0, 0]
curServoPos = {"0":0, "1":60}

class interface:
    """ i2c based comm protocol
        each transaction is divided in 3 steps
        1. send command (1 byte)
        2. send data (1 byte)
        3. receive response (1 byte)
    """
    I2C_DELAY = 0.01
    CMD_SET_LSPEED = 0
    CMD_SET_RSPEED = 1
    
    def processCmd(self, cmd, data):
        bus.write_byte(address, cmd & 0xff)
        time.sleep(self.I2C_DELAY)
        bus.write_byte(address, data & 0xff)
        time.sleep(selfI2C_DELAY)
        res = bus.read_byte(address)
        return res

    def setRoverSpeed(ls, rs):
        logger.info("setRoverSpeed (%d, %d)" % (ls, rs))
        processCmd(CMD_SET_LSPEED, ls)
        processCmd(CMD_SET_RSPEED, rs)
        curRoverSpeed = [ls, rs]

    def setCameraPos(pan, tilt):
        logger.info("setCameraPos (%d, %d)" % (pan, tilt))
        curCamPos = [pan, tilt]

    def setServoPos(sid, pos):
        logger.info("setServoPos (%d, %d)" % (sid, pos))
        if str(sid) is in curServoPos:
            curServoPo.update({str(sid):pos})

    def getRoverSpeed():
        return curRoverSpeed;

    def getCameraPos():
        return curCamPos;
    
    def getServoPos(sid):
        if str(sid) is in curServoPos:
            return curServoPos[str(sid)]
        else:
            return None