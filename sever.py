
import socket
import Queue
from pprint import pprint
import time
import sys
from random import randint

# call by server:
def setupServer():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    # dest, port, set up buffer
def listen():
    #allocating space

