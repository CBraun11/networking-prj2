#helper functions shared by severs and clientsimport socket

class States:
    CLOSED, LISTEN, SYN_RCVD, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, TIME_WAIT, CLOSED, LAST_ACK = range(12)

def fromBitsToString(bits, lengthInByte=0):
    #from stackoverflow
    result = ''
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result


def fromStringToBits(s):
    result = ''
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result

def bitsToDict(s):
    # stringToRtpPacketDict
    #rtpPacketDictToString
    # creating a dictionary, this way we don't need to remember the particular number for each field in the header
    #making it easier to acccess each field in the header
    bitsDict = {}
    bits = stringToBits(s);
    bitsDict["sourcePort"] = int(bits[0:16], 2)
    bitsDict["destPort"] = int(bits[16:32], 2)
    bitsDict["seqNum"] = int(bits[32:64], 2)
    bitsDict["ackNum"] = int(bits[64:96], 2)

    bitsDict["syn"] = int(bits[96], 2)
    bitsDict["ack"] = int(bits[97], 2)
    bitsDict["fin"] = int(bits[98], 2)
    bitsDict["rst"] = int(bits[99], 2)
    bitsDict["windowSize"] = int(bits[100:112], 2)
    bitsDict["checksum"] = int(bits[112:128], 2)
    #128 bits takes 16 characters, thus 16th to the end string are data
    bitsDict["data"] = s[16:]
    return bitsDict

def bitsDictToString(bitsDict):
    result = ""
    keyList = {"sourcePort", "destPort", "seqNum", "ackNum", "syn", "ack", "fin", "rst", "windowSize", "checksum"}
    for key in keyList:
        if (key not in bitsDict):
            bitsDict[key] = 0;
    result += bitsToString(str(bin(bitsDict["sourcePort"]))[2:])
    result += bitsToString(str(bin(bitsDict["destPort"]))[2:])
    result += bitsToString(str(bin(bitsDict["seqNum"]))[2:])
    result += bitsToString(str(bin(bitsDict["ackNum"]))[2:])
    #get bits from them
    b = str(bin(bitsDict["syn"]))[2:] + str(bin(bitsDict["ack"]))[2:] + str(bin(bitsDict["fin"]))[2:] + str(bin(bitsDict["rst"]))[2:]
    result += bitsToString(b)
    result += bitsToString(str(bin(bitsDict["receiveWindowSize"]))[2:], 3) 
    result += bitsToString(str(bin(bitsDict["checksum"]))[2:])
    if "data" in bitsDict:
        result += bitsDict["data"]
    return result

