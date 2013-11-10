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

""" i2c based comm protocol
	each transaction is divided in 3 steps
	1. send command (1 byte)
	2. send data (1 byte)
	3. receive response (1 byte)
"""
I2C_DELAY = 0.04
CMD_SET_LSPEED = 0
CMD_SET_RSPEED = 1
bus = None

SL_ADDR = 0x11

def init():
	global bus
	bus = smbus.SMBus(1)

def processCmd(cmd, data):
	bus.write_byte(SL_ADDR, cmd & 0xff)
	time.sleep(I2C_DELAY)
	bus.write_byte(SL_ADDR, data & 0xff)
	time.sleep(I2C_DELAY)
	res = bus.read_byte(SL_ADDR)
	return res

def setRoverSpeed(ls, rs):
	logger.info("setRoverSpeed (%d, %d)" % (ls, rs))
	processCmd(CMD_SET_LSPEED, ls)
	processCmd(CMD_SET_RSPEED, rs)
	curRoverSpeed = [ls, rs]