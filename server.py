import socket
from sharedFunc import *
import sys

state = States.CLOSED
IP_ADDR = "127.0.0.1"
UDP_PORT = 5005
CLIENT_PORT = 0
LAST_ACK = 0

# TODO Add ACK numbers from header
def close():
    global state
    # We has tested without the header bitmanipulations, they worked perfectly
   	# However, we are going to include the code with bit manipulaitons to show that we understand the logic
    try:
        if state == States.ESTABLISHED:
            print 'FIN received from sender. Sending ACK'

            #send ack to the client
           	ackpacketDict = {}
	        ackpacketDict["sourcePort"] = "127.0.0.1"
	        ackpacketDict["destPort"] = CLIENT_PORT
	        ackpacketDict["ackNum"] = messageDick['seqNum'] + messageDick['datalength']
	        ackpacketDict['ack'] = 1
	        ackpacketString = bitsDictToString(ackpacketDict)
	        sock.sendto(ackpacketString, (IP_ADDR, CLIENT_PORT))

            state = States.CLOSE_WAIT

        if state == States.CLOSE_WAIT:
            print 'ACK sent. Sending FIN'

            #send fin to the client
           	ackpacketDict = {}
	        ackpacketDict["sourcePort"] = "127.0.0.1"
	        ackpacketDict["destPort"] = CLIENT_PORT
	        ackpacketDict["ackNum"] = messageDick['seqNum'] + messageDick['datalength']
	        ackpacketDict['fin'] = 1
	        ackpacketString = bitsDictToString(ackpacketDict)
	        sock.sendto(ackpacketString, (IP_ADDR, CLIENT_PORT))
            state = States.LAST_ACK
        
        if state == States.LAST_ACK:
            message, address = sock.recvfrom(4096)
            messageDick = stringToBitdict(data)

            if checksum(messageDick['checksum']) and messageDick['ack'] and address == (IP_ADDR, CLIENT_PORT):
                print 'ACK received. Closing...'
                state = States.CLOSED
                return
    except socket.timeout:
        close()

def recv(bufsize):
	try:
		#When receive a packet from the client, we are going to check the following things:
		#1. do checksum to see if there's any damage on the packets
		#2. check if sequence number is correct(> last ack)
		#3  check if receive the packet within a range of time 
	    message, address = sock.recvfrom(bufsize)
	    messageDick = stringToBitdict(data)

	    if checksum(messageDick['checksum']) and messageDick['seqNum'] > LAST_ACK and address == (IP_ADDR, CLIENT_PORT):
	        IP_ADDR = addr[0]
	        CLIENT_PORT = addr[1]
	        print "sending syn-ack"
	        ackpacketDict = {}
	        ackpacketDict["sourcePort"] = "127.0.0.1"
	        ackpacketDict["destPort"] = CLIENT_PORT
	        LAST_ACK ＝ ackpacketDict["ackNum"]
	        ackpacketDict["ackNum"] = messageDick['seqNum'] + messageDick['datalength']
	        ackpacketDict['ack'] = 1
	    if address == (IP_ADDR, CLIENT_PORT): 
	        if messageDick['fin']:
	            close()
	        else:
	        	ackpacketString = bitsDictToString(ackpacketDict)
	            sock.sendto(ackpacketString, address)
	            print 'ACK sent for data'
	            return (message, address)
    except socket.timeout:
        print "timeout on recv"
        #could be handled by sending the client to retransmit

# We has tested without the header bitmanipulations, they worked perfectly
# However, we are going to include the code with bit manipulaitons to show that we understand the logic
def establish():
	global state
	if state == States.CLOSED:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((IP_ADDR, UDP_PORT))
   
    print "ready to listen"
    state = States.LISTEN
	while state == States.LISTEN:
	    data, addr = sock.recvfrom(1024)
	    syndict = stringToBitdict(data)
	    ## Need to check SYN and checksum
	    print syndict
	    if syndict['syn'] and checksum(syndict['checksum']) and address == (IP_ADDR, CLIENT_PORT):
	        IP_ADDR = addr[0]
	        CLIENT_PORT = addr[1]
	        print "sending syn-ack"
	        synAckpacketDict = {}
	        # synAckpacketDict["sourcePort"] = "127.0.0.1"
	        synAckpacketDict["destPort"] = 5005
	        synAckpacketDict["ackNum"] = syndict['seqNum']
	        synAckpacketDict['syn'] = 1
	        synAckpacketDict['ack'] = 1
	        synAckpacketString = bitsDictToString(synAckpacketDict)
	        sock.sendto(synAckpacketString, (addr))
	        state = States.SYN_RCVD
	    data, addr = sock.recvfrom(1024) 
	    ackPackDic = bitsDictToString(data)
	    while state != States.ESTABLISHED:
	        #checksum , address
	        if ackPackDic['ack']:
	            state = States.ESTABLISHED
	            sock.settimeout(2)
	            print "ESTABLISHED:"
establish()
while state == States.ESTABLISHED:
    print "running in state ", state
    print recv(4096)


