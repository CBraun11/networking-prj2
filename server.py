import socket
import sharedFunc
import sys

state = sharedFunc.States.CLOSED
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
if state == sharedFunc.States.CLOSED:
	sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	# sock.settimeout(2)
	print "ready to listen"
	state = sharedFunc.States.LISTEN

#ready to listen to clients
while state == sharedFunc.States.LISTEN:
	data, addr = sock.recvfrom(1024)
	## Need to check SYN and checksum
	if "SYN" in data:
		print "sending syn-ack"
		sock.sendto("SYN-ACK", (UDP_IP, UDP_PORT))
		state = sharedFunc.States.SYN_RCVD
	data, addr = sock.recvfrom(1024) 
	if (data == "ACK"):
		state = haredFunc.States.ESTABLISHED
		print "ESTABLISHED:"
while state == haredFunc.States.ESTABLISHED:
	data, addr = sock.recvfrom(1024) 

