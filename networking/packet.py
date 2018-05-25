import socket
from random import randint
from struct import pack
from data import Bin
import protocols

ENC = 'UTF-8'


class Packet:
    def __init__(self):
        self.packets = []
        self.payload = ''

    def add_header(self, a):
        self.packets.append(a)

    def set_payload(self, s):
        self.payload = s

    def compile(self):
        return b''.join([p.compile() for p in self.packets]) + self.payload.encode(ENC)

class IPHeader:
    def __init__(self, source, dest, header_length=5, protocol=socket.IPPROTO_TCP):
        # 4 4 6 2 16 16 4 12 8 8 16 32 32
        self.header = [
            Bin(4, 4)+Bin(header_length, 4),  # IPv4
            Bin(0, 6)+Bin(0, 2),  # Type of Service # Something something congestion
            0,  # Total header length; apparently the kernel fills this
            randint(1, 65535),  # 16-bit ID
            Bin(0, 4)+Bin(0, 12),  # Flags # Fragment offset?
            255,  # TTL in hops
            protocol,
            0,  # Checksum; apparently the kernel fills this
            socket.inet_aton(source),
            socket.inet_aton(dest)
        ]

    def compile(self):
        return pack('!BBHHHBBH4s4s', *self.header)


class ICMPHeader:
    def __init__(self, type=0, subtype=0, header_data=0):
        # 8 8 16 32
        self.header = [
            type,  # Type; echo is 0
            subtype,  # Subtype
            0,  # Checksum; apparently the kernel fills this
            header_data  # Varies by action; usually ID and Seq Num
        ]

    def compile(self):
        return pack('!BBHI', *self.header)

if __name__ == '__main__':
    print('Creating packet...')
    p = Packet()
    p.add_header(IPHeader('192.168.1.164', '192.168.1.173', protocol=protocols.ICMP))
    p.add_header(ICMPHeader(header_data=Bin(randint(1, 65535), 16)+Bin(randint(1, 65535), 16)))
    p.set_payload('hello world')
    print(p.compile())
    print('Done.')
