import socket
import sharedFunc
import sys

state = sharedFunc.States.CLOSED

# Add command line input

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

MAX_LENGTH = 4096

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


def connect():  
    print 'In connect'
    sock.sendto('SYN', (UDP_IP, UDP_PORT))
    state = sharedFunc.States.SYN_SENT
    print 'SYN sent'

    while True:
        message, address = sock.recvfrom(1024)
        if address == (UDP_IP, UDP_PORT) and 'SYN-ACK' in message:
            print 'SYN-ACK received'
            state = sharedFunc.States.ESTABLISHED
            break

    sock.sendto('ACK', (UDP_IP, UDP_PORT))
    print 'ACK sent'

connect()