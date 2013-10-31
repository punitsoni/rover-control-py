#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys

host = 'localhost'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
sys.stdout.write('%')

while 1:
    # read from keyboard
    line = sys.stdin.readline()
    if line == '\n':
        break
    s.send(line.rstrip())
    data = s.recv(size)
    sys.stdout.write(data + "\n")
    sys.stdout.write('%')
s.close()
