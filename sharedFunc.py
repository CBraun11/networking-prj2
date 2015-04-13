# This file contains helper functions, mainly as an interface to the RxP header. 
# We had issues with the implementation of bit manipulation in
# Python, but we leave our attempt to show our logic.

import binascii
from random import randint


MAX_LENGTH = 4096

# State definitions.
class States:
    CLOSED, LISTEN, SYN_RCVD, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, TIME_WAIT, CLOSED, LAST_ACK = range(12)

# Checksum implementation.
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff


# helper functions to get convert character strings to bitstrings and vice versa.
def stringToBits(s):
    result = ''
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result

def bitsToString(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


# Function that converts a string from the network into a dictionary for easy access and edits.
def stringToBitdict(s):
    # Create a dictionary, this way we don't need to remember the particular number for each field in the header
    # Making it easier to acccess each field in the header
    bitsDict = {}
    bits = stringToBits(s);
    bitsDict["sourcePort"] = int(bits[0:16], 2)
    bitsDict["destPort"] = int(bits[16:32], 2)
    bitsDict["seqNum"] = int(bits[32:64], 2)
    bitsDict["ackNum"] = int(bits[64:96], 2)

    bitsDict["syn"] = int(bits[96:104], 2)
    bitsDict["ack"] = int(bits[104:112], 2)
    bitsDict["fin"] = int(bits[112:120], 2)
    bitsDict["rst"] = int(bits[120:128], 2)

    bitsDict['datalength'] = int(bits[128:144], 2)
    bitsDict["windowSize"] = int(bits[144:160], 2)
    bitsDict["checksum"] = int(bits[160:176], 2)

    bitsDict["data"] = s[24:]
    return bitsDict

def bitsDictToString(bitsDict):

    result = ""
    keyList = {"sourcePort", "destPort", "seqNum", "ackNum", "syn", "ack", "fin", "rst", 'datalength',  "windowSize", "checksum"}
    for key in keyList:
        if (key not in bitsDict):
            bitsDict[key] = 0;
    result += str(bitsDict["sourcePort"])
    result += str(bitsDict["destPort"])
    result += str(bitsDict["seqNum"])
    result += str(bitsDict["ackNum"])
    result += str(bitsDict["syn"])
    result += str(bitsDict["ack"])
    result += str(bitsDict["fin"])
    result += str(bitsDict["rst"])

    result += str(bitsDict["datalength"])
    result += str(bitsDict["windowSize"])
    result += str(bitsDict["checksum"])
 
    if "data" in bitsDict:
        result += bitsDict["data"]
    return result


