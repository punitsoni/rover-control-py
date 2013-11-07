#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys

host = 'localhost'
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "connecting to server..."
s.connect((host,port))
print "connected"

testMsg = ([4, 0, 0, 0, 0, 97, 98, 99],
           [4, 0, 0, 0, 0, 66, 67, 68],
           [4, 0, 0, 0, 1, 0, 60, 70])
           
N = len(testMsg)
i=0

while 1:
    sys.stdout.write('% ')
    line = sys.stdin.readline()
    if line == 'exit\n':
        break
    print "sending test msg %d : %s" % (i%N, str(testMsg[i%N]))
    s.send(''.join(map(chr, testMsg[i%N])))
    data = s.recv(1024)
    if data == None:
        print "server disconnected"
        break
    
    rx_bytes = map(ord, data)
    
    print "received: ", str(rx_bytes)
    
    #sys.stdout.write(data + "\n")
    i += 1
s.close()
