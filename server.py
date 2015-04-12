import socket
import sharedFunc
import sys

state = sharedFunc.States.CLOSED
IP_ADDR = "127.0.0.1"
UDP_PORT = 5005
CLIENT_PORT = 0



def recv(bufsize):
    ## TODO Implement checksum and verify
    ## TODO Implement and verify sequence number
    # TODO Implement receiver queue
    message, address = sock.recvfrom(bufsize)
    sock.sendto('ACK', address)
    print 'ACK sent for data'
    return (message, address)
    

if state == sharedFunc.States.CLOSED:
    sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
    sock.bind((IP_ADDR, UDP_PORT))
	# sock.settimeout(2)
    print "ready to listen"
    state = sharedFunc.States.LISTEN

#ready to listen to clients
while state == sharedFunc.States.LISTEN:
    data, addr = sock.recvfrom(1024)
	## Need to check SYN and checksum
    if "SYN" in data:
        IP_ADDR = addr[0]
        CLIENT_PORT = addr[1]
        print "sending syn-ack"
        sock.sendto('SYN-ACK', (addr))
        state = sharedFunc.States.SYN_RCVD
    data, addr = sock.recvfrom(1024) 
    while state != sharedFunc.States.ESTABLISHED:
        if (data == "ACK"):
            state = sharedFunc.States.ESTABLISHED
            print "ESTABLISHED:"

while state == sharedFunc.States.ESTABLISHED:
    print "running"
    print recv(4096)




