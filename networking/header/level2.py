import socket
from .data import *
from random import randint
from struct import pack

class MACHeader:
    def __init__(self, src_mac, dst_mac, ethertype):
        self.header = [
            b''.join([chr(int(c, 16)).encode(ENC) for c in dst_mac.split(':')]),
            b''.join([chr(int(c, 16)).encode(ENC) for c in src_mac.split(':')]),
            ethertype
        ]

    def compile(self):
        return pack('!6s6sH', *self.header)


class ARPHeader:
    def __init__(self):
        ...