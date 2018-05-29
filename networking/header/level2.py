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
    def __init__(self):
        ...
