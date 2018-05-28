import socket
from .data import *
from random import randint
from struct import pack

class IPHeader:
    def __init__(self, source, dest, header_length=5, ttl=255, protocol=socket.IPPROTO_TCP):
        # 4 4 6 2 16 16 4 12 8 8 16 32 32
        self.src = source
        self.dst = dest
        self.header = [
            Bin(4, 4)+Bin(header_length, 4),  # IPv4 (8)
            Bin(0, 6)+Bin(0, 2),  # Type of Service # Something something congestion (8)
            0,  # Total packet length (16)
            randint(0, 0xFFFF),  # 16-bit ID (16)
            Bin(0, 4)+Bin(0, 12),  # Flags # Fragment offset? (16)
            ttl,  # TTL in hops (8)
            protocol, # (8)
            0,  # Checksum (16)
            socket.inet_aton(source),  # (32)
            socket.inet_aton(dest)  # (32)
        ]

    def compile(self):
        self.header[-3] = 0
        debug = False
        # Find checksum
        # Reference table for adding padding 0's
        data_sizes = [8, 8, 16, 16, 16, 8, 8, 16, 32, 32]

        # Convert IP addresses to integers
        h = self.header[:-2] + [
            int(''.join(['0' * (8 - len(bin(c)[2:])) + bin(c)[2:] for c in socket.inet_aton(self.src)]), 2),
            int(''.join(['0' * (8 - len(bin(c)[2:])) + bin(c)[2:] for c in socket.inet_aton(self.dst)]), 2)]

        # Grabs every header item and converts to hex; adds padding 0's too
        c = binpad(h, data_sizes)
        c = cut(c, 16)
        if debug: print(0, c)

        # Splits the header into 16-bit words, sums them, and converts it to binary
        b = checksum(c)

        # Convert to int for packing
        if debug: print(5, b)
        self.header[-3] = b

        return pack('!BBHHHBBH4s4s', *self.header)