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
    # We have tested without the header bit manipulations, they worked perfectly;
    # However, we include the attempted bit manipulaitons to show that we understand the logic.
    try:
        if state == States.ESTABLISHED:
            print 'FIN received from sender. Sending ACK'

            # Received FIN. Send ack to the client.
           	ackpacketDict = {}
	        ackpacketDict["sourcePort"] = "127.0.0.1"
	        ackpacketDict["destPort"] = CLIENT_PORT
	        ackpacketDict["ackNum"] = messageDict['seqNum'] + messageDict['datalength']
	        ackpacketDict['ack'] = 1
	        ackpacketString = bitsDictToString(ackpacketDict)
	        sock.sendto(ackpacketString, (IP_ADDR, CLIENT_PORT))

            state = States.CLOSE_WAIT

        if state == States.CLOSE_WAIT:
            print 'ACK sent. Sending FIN'

            # Send FIN to the client.
           	ackpacketDict = {}
	        ackpacketDict["sourcePort"] = "127.0.0.1"
	        ackpacketDict["destPort"] = CLIENT_PORT
	        ackpacketDict["ackNum"] = messageDict['seqNum'] + messageDict['datalength']
	        ackpacketDict['fin'] = 1
	        ackpacketString = bitsDictToString(ackpacketDict)
	        sock.sendto(ackpacketString, (IP_ADDR, CLIENT_PORT))
            state = States.LAST_ACK

        # Receive the last ACK from the client
        if state == States.LAST_ACK:
            message, address = sock.recvfrom(4096)
            messageDict = stringToBitdict(data)

            if checksum(messageDict['checksum']) and messageDict['ack'] and address == (IP_ADDR, CLIENT_PORT):
                print 'Last ACK received. Closing...'
                state = States.CLOSED
                return
    except socket.timeout:
        close()

def recv(bufsize):
	try:
		# When we receive a packet from the client, we are going to check the following things:
		# 1. The checksum, to see if there's any damage to the packet
		# 2. The correctness of the sequence number(> last ack)

	    message, address = sock.recvfrom(bufsize)
	    messageDict = stringToBitdict(data)

	    if checksum(messageDict['checksum']) and messageDict['seqNum'] > LAST_ACK and address == (IP_ADDR, CLIENT_PORT):
	        IP_ADDR = addr[0]
	        CLIENT_PORT = addr[1]
	        print "Sending SYN-ACK"
	        ackpacketDict = {}
	        ackpacketDict["sourcePort"] = "127.0.0.1"
	        ackpacketDict["destPort"] = CLIENT_PORT
	        LAST_ACK ＝ ackpacketDict["ackNum"]
	        ackpacketDict["ackNum"] = messageDict['seqNum'] + messageDict['datalength']
	        ackpacketDict['ack'] = 1
	    if address == (IP_ADDR, CLIENT_PORT): 

		    # Upon getting a FIN, close the connection gracefully.
	        if messageDict['fin']:
	            close()
            # Otherwise, treat it like a normal message
	        else:
	            ackpacketString = bitsDictToString(ackpacketDict)
	            sock.sendto(ackpacketString, address)
	            print 'ACK sent for data'
	            return (message, address)
    except socket.timeout:
        print "timeout on recv"

# We has tested without the header bitmanipulations, they worked perfectly
# However, we are going to include the code with bit manipulaitons to show that we understand the logic
def establish():
	global state
	if state == States.CLOSED:
    sock = socket.socket(socket.AF_INET, # IP
                         socket.SOCK_DGRAM) # UDP
    sock.bind((IP_ADDR, UDP_PORT))
   
    print "Listening..."
    state = States.LISTEN
	while state == States.LISTEN:
        # Check for a SYN packet
	    data, addr = sock.recvfrom(1024)
	    syndict = stringToBitdict(data)
	    if syndict['syn'] and checksum(syndict['checksum']) and address == (IP_ADDR, CLIENT_PORT):
            #If we receive a SYN while in this state, reply with a SYN-ACK
	        IP_ADDR = addr[0]
	        CLIENT_PORT = addr[1]
	        print "Sending SYN-ACK"
	        synAckpacketDict = {}
	        synAckpacketDict["sourcePort"] = "127.0.0.1"
	        synAckpacketDict["destPort"] = 5005
	        synAckpacketDict["ackNum"] = syndict['seqNum']
	        synAckpacketDict['syn'] = 1
	        synAckpacketDict['ack'] = 1
	        synAckpacketString = bitsDictToString(synAckpacketDict)
	        sock.sendto(synAckpacketString, (addr))
	        state = States.SYN_RCVD

        # After sending SYN-ACK, wait for an ACK to confirm connection establishment..
	    data, addr = sock.recvfrom(1024) 
	    ackPackDic = bitsDictToString(data)
	    while state != States.ESTABLISHED:
	        if ackPackDic['ack']:
	            state = States.ESTABLISHED
	            sock.settimeout(2)
	            print "Established."



# Test case. This code constantly receives data.
establish()
while state == States.ESTABLISHED:
    print recv(4096)


