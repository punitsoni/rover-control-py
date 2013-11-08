#!/usr/bin/python

import logging

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

def setRoverSpeed(ls, rs):
    logger.info("setRoverSpeed (%d, %d)" % (ls, rs))
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


