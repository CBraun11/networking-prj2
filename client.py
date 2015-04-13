import socket
from sharedFunc import *
import sys
import time
from random import randint

state = States.CLOSED

# Add command line input

IP_ADDR = "127.0.0.1"
SERVER_PORT = 5005

MAX_MESSAGE_LENGTH = 4096
HEADER_LENGTH = 24

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.settimeout(2)

sourcePort = 8080

def connect():
    #to connect to the server, we have 3 way handshake
    #1. the client sends SYN to the server
    #2. Upon received the syn at the server side, the server will send ack + syn to the client
    #3. Lastly the client sends ack to the server and finish the establishment 
    global state  
    print 'Connecting...'

    # Building Packet
    initialSeqNum = randint(0, 20000)
    synpacketDict = {}
    for key in keyList:
        synpacketDict[key] = 0
    synpacketDict["sourcePort"] = sourcePort
    synpacketDict["destPort"] = 5005
    synpacketDict["seqNum"] = initialSeqNum
    synpacketDict['syn'] = 1
    synpacketString = bitsDictToString(synpacketDict)

    # Sending SYN
    sock.sendto(synpacketString, (IP_ADDR, SERVER_PORT))
    state = States.SYN_SENT
    print 'SYN sent'

    # Receiving SYN-ACK
    while True:
        message, address = sock.recvfrom(1024)
        synACKdict = stringToBitdict(message)
        #client checks the packet
        if synACKdict['ack'] and synACKdict['syn'] and synACKdict['ackNum'] == initialSeqNum and checksum(synACKdict['checksum']):
            print 'SYN-ACK received'
            state = States.ESTABLISHED
            break


    # Sending ACK
    ackpacketDict["seqNum"] = initialSeqNum
    ackpacketDict['ackNum'] = synACKdict['seqNum']
    ackpacketDict["sourcePort"] = sourcePort
    ackpacketDict["destPort"] = 5005
    ackpacketDict['ack'] = 1
    sock.sendto(ackpacketDict, (IP_ADDR, SERVER_PORT))
    print 'ACK sent'

def send(message):
    
    try:
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

    
def close():
    global state
    #TODO ADD HEADER FIELDS
    try:
        if state == States.ESTABLISHED:
            # Send FIN
            ackpacketDict = {}
            ackpacketDict["sourcePort"] = "127.0.0.1"
            ackpacketDict["destPort"] = CLIENT_PORT
            ackpacketDict["ackNum"] = messageDict['seqNum'] + messageDict['datalength']
            ackpacketDict['fin'] = 1
            ackpacketString = bitsDictToString(ackpacketDict)
            sock.sendto(ackpacketString, (IP_ADDR, SERVER_PORT))
            
            print 'Sent FIN'
            state = States.FIN_WAIT_1
        # Look for FIN and ACK
        if state == States.FIN_WAIT_1:
            response, address = sock.recvfrom(MAX_MESSAGE_LENGTH)
            if address == (IP_ADDR, SERVER_PORT):
                if 'ACK' in response:
                    print 'ACK received.'
                    state = States.FIN_WAIT_2

        if state == States.FIN_WAIT_2:
            response, address = sock.recvfrom(MAX_MESSAGE_LENGTH)
            if address == (IP_ADDR, SERVER_PORT):
                if 'FIN' in response:
                    print 'FIN received. Sending ACK...'
                    sock.sendto('ACK', (IP_ADDR, SERVER_PORT))
                    state = States.TIME_WAIT
                    time.sleep(1)
                    print 'Closing...'
                    return


        # Wait
        if state == States.TIME_WAIT:
            time.sleep(1)
            return
    except socket.timeout:
        close()


# Test connection establishment and message
connect()
send('hello world')
close()

