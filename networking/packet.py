import socket
from random import randint
from struct import pack
from data import Bin
import protocols

ENC = 'UTF-8'


class Packet:
    def __init__(self, dest, src=socket.gethostbyname(socket.gethostname())):
        self.headers = []
        self.dest = dest
        self.src = src
        self.payload = ''

    def add_header(self, a):
        self.headers.append(a)

    def set_payload(self, s):
        self.payload = s

    def compile(self):
        return b''.join([p.compile() for p in self.headers]) + self.payload.encode(ENC)

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dest

class IPHeader:
    def __init__(self, source, dest, header_length=5, protocol=socket.IPPROTO_TCP):
        # 4 4 6 2 16 16 4 12 8 8 16 32 32
        self.src = source
        self.dst = dest
        self.header = [
            Bin(4, 4)+Bin(header_length, 4),  # IPv4
            Bin(0, 6)+Bin(0, 2),  # Type of Service # Something something congestion
            0,  # Total header length; apparently the kernel fills this
            randint(0, 0xFFFF),  # 16-bit ID
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
    def __init__(self, type=0, subtype=0, seq=randint(0, 0xFFFF), id=randint(0, 0xFFFF)):
        # 8 8 16 32
        self.header = [
            type,  # Type; echo is 0
            subtype,  # Subtype
            0,  # Checksum; apparently the kernel fills this
            id,
            seq
        ]

    def compile(self):
        return pack('!BBHHH', *self.header)


class TCPHeader:
    def __init__(self):
        ...


if __name__ == '__main__':
    print('Creating ICMP packet...')
    p = Packet('192.168.1.173')
    #p.add_header(IPHeader('192.168.1.164', '192.168.1.173', protocol=protocols.ICMP))
    p.add_header(ICMPHeader(id=randint(1, 0xFFFF), seq=1))
    p.set_payload('hello world')
    print(p.compile())
    print('Initializing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    print('Sending...')
    s.sendto(p.compile(), (p.get_dst(), 0))
    print('Packet sent, awaiting response...')
    print('Response:', s.recvfrom(1024))
    print('Operation complete.')
