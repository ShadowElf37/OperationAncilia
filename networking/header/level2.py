import socket
from .data import *
from random import randint
from struct import pack

class MACHeader:
    def __init__(self, src_mac, dst_mac, ethertype):
        self.header = [
            *[int(c, 16) for c in dst_mac.split(':')],
            *[int(c, 16) for c in src_mac.split(':')],
            ethertype
        ]

    def compile(self):
        return pack('!BBBBBBBBBBBBH', *self.header)


class ARPHeader:
    def __init__(self, src_ip, src_maddr, dst_ip, ethertype, dst_maddr=0, operation=1):
        self.header = [
            1,
            ethertype,
            6,
            4,
            operation,  # Can be 1 or 2; req or reply
            *[int(c, 16) for c in src_maddr.split(':')],
            socket.inet_aton(src_ip),
            *([int(c, 16) for c in dst_maddr.split(':')] if dst_maddr != 0 else [0]*6),
            socket.inet_aton(dst_ip)
        ]

    def compile(self):
        return pack('!HHBBH'+('B'*6+'4s')*2, *self.header)
