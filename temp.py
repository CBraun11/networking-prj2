import binascii
import math

#helper functions shared by severs and clientsimport socket
MAX_LENGTH = 4096
class States:
    CLOSED, LISTEN, SYN_RCVD, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, TIME_WAIT, CLOSED, LAST_ACK = range(12)


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

def stringToBitdict(s):
    # stringToRtpPacketDict
    #rtpPacketDictToString
    # creating a dictionary, this way we don't need to remember the particular number for each field in the header
    #making it easier to acccess each field in the header
    bitsDict = {}
    bits = stringToBits(s);
    # print int(bits[96:97], 2)
    bitsDict["sourcePort"] = int(bits[0:16], 2)
    bitsDict["destPort"] = int(bits[16:32], 2)
    bitsDict["seqNum"] = int(bits[32:64], 2)
    bitsDict["ackNum"] = int(bits[64:96], 2)

    bitsDict["syn"] = int(bits[96], 2)
    bitsDict["ack"] = int(bits[97], 2)
    bitsDict["fin"] = int(bits[98], 2)
    bitsDict["rst"] = int(bits[99], 2)
    bitsDict['datalength'] = int(bits[100:112], 2)
    bitsDict["windowSize"] = int(bits[112:128], 2)
    bitsDict["checksum"] = int(bits[128:144], 2)
    #144 bits takes 18 characters, thus 16th to the end string are data
    bitsDict["data"] = s[18:]
    return bitsDict

def bitsDictToString(bitsDict):

    result = ""
    keyList = {"sourcePort", "destPort", "seqNum", "ackNum", "syn", "ack", "fin", "rst", 'datalength',  "windowSize", "checksum"}
    for key in keyList:
        if (key not in bitsDict):
            print "is it exist?"
            bitsDict[key] = 0;
    result += binascii.unhexlify('%x' % bitsDict["sourcePort"]) 
    result += binascii.unhexlify('%x' % bitsDict["destPort"]) 
    result += binascii.unhexlify('%x' % bitsDict["sourcePort"]) 
    result += binascii.unhexlify('%x' % bitsDict["seqNum"]) 
    result += binascii.unhexlify('%x' % bitsDict["ackNum"]) 

    bs = str(bin(bitsDict["syn"])[2:])  + str(bin(bitsDict["ack"])[2:])  + str(bin(bitsDict["fin"])[2:]) + str(bin(bitsDict["rst"])[2:]) + str(bin(bitsDict["datalength"])[2:]) 
    
    print str(bin(bitsDict["ack"])[2:])
    print str(bin(bitsDict["syn"])[2:])
    print str(bin(bitsDict["rst"])[2:])
    print str(bin(bitsDict["fin"])[2:])
    print str(bin(bitsDict["datalength"])[2:])

    bs =  int(bs.replace(' ', ''), 2)
    print bs
    bs = 3426
    result += binascii.unhexlify('%x' % bs)
    # result += bitsToString(b)
    result += binascii.unhexlify('%x' % bitsDict["windowSize"]) 
    result += binascii.unhexlify('%x' % bitsDict["checksum"]) 
    if "data" in bitsDict:
        result += bitsDict["data"]
    print "result is : "
    return result

# def numberOfPackets(data):
#     numPackets = 1
#     if len(data) + 20 > MAX_LENGTH:
#         numPackets = int(len(data)/(MAX_LENGTH-20))
#         if len(data) % (MAX_LENGTH-20) != 0:
#             numPackets += 1
#     return numPackets


# print "teting bitdic to String" + bitsDictToString(bitsToDict('abcdefg8abcdefg8ab'))
# print "testing string to bits" + stringToBits('0011000100110001001100000011000000110000001100000011000100110000001100010011000100110000001100000011000000110001001100000011000100110001001100000011000000110000001100010011000100110000001100010011000100110000001100000011000100110000001100000011000100110001001100000011000000110001001100000011000100110000001100010011000100110000001100000011000100110001001100000011000000110001001100010011000000110000001100010011000100110001001100000011000000110001001100010011000100110000001100000011000000110001001100010011000000110000001100000011000000110001001100000011000100110001001100000011000000110000001100010011000000110000001100010011000100110000001100000011000000110001001100010011000000110001001100010011000000110000001100010011000000110000001100000011000100110001001100000011000100110000001100010011000000110001001100010011000000110000001100010011000100110000001100010011000100110000001100000011000100110001001100010011000000110000001100010011000100110001001100000011000000110000ab')


tempDict = stringToBitdict('abcdababefg8abfg8abc90')
print tempDict
print bitsDictToString(tempDict)
# 0110101100010
# tempDict['ack'] = int(0,2)
# print tempDict
# print bitsDictToString(tempDict)

# print 
