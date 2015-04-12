import socket
import sharedFunc
import sys

state = sharedFunc.States.CLOSED

# Add command line input

IP_ADDR = "127.0.0.1"
SERVER_PORT = 5005

MAX_MESSAGE_LENGTH = 4096
HEADER_LENGTH = 18

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.settimeout(2)


def connect():  
    print 'In connect'
    sock.sendto('SYN', (IP_ADDR, SERVER_PORT))
    state = sharedFunc.States.SYN_SENT
    print 'SYN sent'

    while True:
        message, address = sock.recvfrom(1024)
        if 'SYN-ACK' in message:
            print 'SYN-ACK received'
            state = sharedFunc.States.ESTABLISHED
            break

    sock.sendto('ACK', (IP_ADDR, SERVER_PORT))
    print 'ACK sent'


def send(message):
    # TODO Implement and verify ACK number
    try:
        #timer

        if len(message) > MAX_MESSAGE_LENGTH:
            message = message[:MAX_MESSAGE_LENGTH - HEADER_LENGTH] # Only send the first MAX_MESSAGE_LENGTH bytes
        sock.sendto(message, (IP_ADDR, SERVER_PORT))

        #ACK
        response, address = sock.recvfrom(MAX_MESSAGE_LENGTH)
        if address == (IP_ADDR, SERVER_PORT):
            if 'ACK' in response:
                print 'ACK received'
                return len(message)
            

    except socket.timeout:
        send(message)

    
        
    


connect()
send('hello world')
