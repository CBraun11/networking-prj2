import socket
import sys
import time

class States:
    CLOSED, LISTEN, SYN_RCVD, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, TIME_WAIT, CLOSED, LAST_ACK = range(12)

state = States.CLOSED
MAX_MESSAGE_LENGTH = 4096
HEADER_LENGTH = 18
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.settimeout(2)
Clinet_IP = None
Server_IP = None
Server_PORT = None
CLIENT_PORT = None


def setupServer():
    global state
    global Server_IP
    global Server_PORT
    Server_IP = "127.0.0.1"
    Server_PORT = 5005
    listen()

# TODO Add ACK numbers from header
def close():
    try:
        if state == States.ESTABLISHED:
            print 'FIN received from sender. Sending ACK'
            sock.sendto('ACK', (Clinet_IP, CLIENT_PORT))
            state  = States.CLOSE_WAIT

        if state  == States.CLOSE_WAIT:
            print 'ACK sent. Sending FIN'
            sock.sendto('FIN', (Clinet_IP, CLIENT_PORT))
            state  = States.LAST_ACK
        
        if state  == States.LAST_ACK:
            message, address = sock.recvfrom(4096)
            if 'ACK' in message and address == (Clinet_IP, CLIENT_PORT):
                print 'ACK received. Closing...'
                state  = States.CLOSED
                return
    except socket.timeout:
        close()

def recv(bufsize):
    ## TODO Implement checksum and verify
    ## TODO Implement and verify sequence number
    # TODO Implement receiver queue
    message, address = sock.recvfrom(bufsize)
    # TODO sequence number verification
    if address == (Clinet_IP, CLIENT_PORT): 
        if 'FIN' in message:
            close()
        else:
            sock.sendto('ACK', address)
            print 'ACK sent for data'
            return (message, address)

def listen():
    global state

    if state == States.CLOSED:
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        print Server_IP
        sock.bind((Server_IP, Server_PORT))
        # sock.settimeout(2)
        print "ready to listen"
        state = States.LISTEN

    #ready to listen to clients
    while state == States.LISTEN:
        data, addr = sock.recvfrom(1024)
        ## Need to check SYN and checksum
        if "SYN" in data:
            Clinet_IP = addr[0]
            CLIENT_PORT = addr[1]
            print "sending syn-ack"
            sock.sendto('SYN-ACK', (addr))
            state = States.SYN_RCVD
        data, addr = sock.recvfrom(1024) 
        while state != States.ESTABLISHED:
            if (data == "ACK"):
                state = States.ESTABLISHED
                print "ESTABLISHED:"



setupServer()
while state == States.ESTABLISHED:
    print "running in state ", state

