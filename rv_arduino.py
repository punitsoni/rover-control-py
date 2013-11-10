#!/usr/bin/python

import smbus
import sys
import time

bus = smbus.SMBus(1)

address = 0x11

I2C_DELAY = 0.01

def sendMsg(msg):
    for b in msg:
        print "writing byte %d" % (b & 0xff)
        bus.write_byte(address, b & 0xff)

def receiveData():
    data = 0;
    for i in range(0, 4):
        b = bus.read_byte(address)
        print "b[%d] = %d" % (i, b)
        data += (b << 8*i)
    return data;

def processCmd(cmd, data):
    # send command
    bus.write_byte(address, cmd & 0xff)
    time.sleep(I2C_DELAY)
    # send data
    bus.write_byte(address, data & 0xff)
    time.sleep(I2C_DELAY)
    # request response
    res = bus.read_byte(address)
    return res

cmd_list = [[0, 20], [1, 50], [3, 6]]
N = len(cmd_list);
i = 0
while True:
    sys.stdout.write("% ")
    line = sys.stdin.readline()
    if line == "exit\n":
        break
    print "process cmd ", i, " ", cmd_list[i]
    val = processCmd(cmd_list[i][0], cmd_list[i][1])
    i += 1
    if i == N:
        i = 0;
    print "val = ", val