#!/usr/bin/python

import smbus
import time
import sys

bus = smbus.SMBus(1)

address = 0x11

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number

def sendMsg(msg):
    for b in msg:
        writeNumber(b)

def receiveData():
    data = 0;
    for i in range(0, 4):
        b = bus.read_byte(address)
        print "b[%d] = %d" % (i, b)
        data += (b << 8*i)
    return data;


while True:
    sys.stdout.write("% ")

    line = sys.stdin.readline()
    if line == "exit\n":
        break

    number = receiveData()
    #number = readNumber()
    print "status = ", number
