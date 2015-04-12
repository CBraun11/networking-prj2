#helper functions shared by severs and clientsimport socket

class States:
    CLOSED, LISTEN, SYN_RCVD, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, TIME_WAIT, CLOSED, LAST_ACK = range(12)

def fromBitsToString(bits, lengthInByte=0):
    # make sure the output string is of correct length
    if (len(bits) < lengthInByte * 8):
        bits = str('0' * (lengthInByte * 8 - len(bits))) + bits
    else:
        if (lengthInByte != 0 and len(bits) > lengthInByte * 8):
            bits = bits[-lengthInByte * 8:]

    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

    return ''.join(chars)


def fromStringToBits(s):
    result = ''
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result

