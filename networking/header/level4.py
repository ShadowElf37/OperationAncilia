import socket
from .data import *
from random import randint
from struct import pack

class ICMPHeader:
    def __init__(self, payload, type=0, subtype=0, seq=randint(0, 0xFFFF), id=randint(0, 0xFFFF)):
        # 8 8 16 16 16
        self.header = [
            type,  # Type; echo is 0 or 8
            subtype,  # Subtype
            0,  # Checksum
            id,
            seq
        ]
        self.payload = payload

    def compile(self):
        self.header[2] = 0
        debug = False
        # Padding reference table
        data_sizes = [8, 8, 16, 16, 16]
        # Hexify and pad
        chk = binpad(self.header, data_sizes)
        chk = cut(chk, 16)

        # Add payload
        if debug: print(1, chk)
        i = 0
        l = []
        t = ''
        for c in self.payload:
            i += 1
            a = bin(ord(c))[2:]
            t += '0' * (len(a)%2) + a
            if i % 2 == 0:
                l.append(t)
                t = ''
        chk += l
        if debug: print(2, chk)

        # Splits, sums, returns binary
        n = checksum(chk)

        # Pack
        if debug: print(5, n)
        self.header[2] = n
        return pack('!BBHHH', *self.header)


class TCPHeader:
    def __init__(self, src_port, dst_port, seq=randint(0, 0xFFFF), NS=0, CWR=0, ECE=0, URG=0, ACK=0, PSH=0, RST=0, SYN=0, FIN=0, ACK_NUM=0, URG_NUM=0):
        # 16 16 32 32 4+3+1 8 16 16 16
        self.header = [
            src_port,
            dst_port,
            seq,
            ACK_NUM,  # ACK number
            Bin(5, 4) + Bin(Bin(0, 3) + Bin(NS, 1), 4),  # Data offset # Reserved by protocol # Flag
            int(''.join([str(n) for n in [CWR,ECE,URG,ACK,PSH,RST,SYN,FIN]]), 2),  # More flags
            socket.htons(5840),  # Window size??? Apparently this is max value
            0,  # Checksum
            URG_NUM
        ]

    def compile(self):
        return pack('!HHLLBBHHH', *self.header)


class UDPHeader:
    def __init__(self):
        ...