#!/usr/bin/python

import smbus
import sys
import time

bus = smbus.SMBus(1)

address = 0x11

I2C_DELAY = 0.05

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
speed = 0
while True:
    sys.stdout.write("% ")
    line = sys.stdin.readline()
    if line == "exit\n":
        break
    s = line.strip().split();
    cmd = int(s[0]);
    data = int(s[1]);
    print "cmd, data = ", [cmd, data]
    val = processCmd(cmd, data)
    print "response = ", val