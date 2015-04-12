import socket
import sharedFunc
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Add command line input

state = sharedFunc.States.CLOSED

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def listen():
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    if data == "SYN":
        print 'SYN Received' 
    else:
        print 'Invalid input'

listen()



