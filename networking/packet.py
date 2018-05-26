import socket
from random import randint
from struct import pack
from data import *
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
            65535,  # Total packet length
            randint(0, 0xFFFF),  # 16-bit ID
            Bin(0, 4)+Bin(0, 12),  # Flags # Fragment offset?
            255,  # TTL in hops
            protocol,
            0,  # Checksum
            socket.inet_aton(source),
            socket.inet_aton(dest)
        ]

        # Find checksum
        h = self.header[:-2] + [int(''.join([str(bin(ord(c)))[2:] for c in str(socket.inet_aton(source))]), 2),
            int(''.join([str(bin(ord(c)))[2:] for c in str(socket.inet_aton(dest))]), 2)]
        b = str(bin(sum(list(map(lambda x: int(x, 16), cut(''.join([str(hex(i))[2:] for i in h]), 4))))))[2:]
        # print(1, b)
        b = cut(b, 4)
        # print(2, b)
        while len(b) > 4:
            b = str(bin(int(b[0], 2) + int(''.join(b[-4:]), 2)))[2:]
            # print(3, b)
            b = cut('0'*(len(b)%4) + b, 4)
        # print(4, int(''.join(b), 2))
        n = ''
        for c in ''.join(b):
            if c == '1':
                n += '0'
            else:
                n += '1'
        b = int(n, 2)
        print(5, hex(b))
        self.header[-3] = b


    def compile(self):
        return pack('!BBHHHBBH4s4s', *self.header)


class ICMPHeader:
    def __init__(self, type=0, subtype=0, seq=randint(0, 0xFFFF), id=randint(0, 0xFFFF)):
        # 8 8 16 32
        self.header = [
            type,  # Type; echo is 0
            subtype,  # Subtype
            0,  # Checksum
            id,
            seq
        ]

    def compile(self):
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


class ARPHeader:
    def __init__(self):
        ...


if __name__ == '__main__':
    print('Creating TCP packet...')
    p = Packet('192.168.1.173')
    p.add_header(IPHeader('192.168.1.164', '192.168.1.173', protocol=protocols.ICMP))
    p.add_header(ICMPHeader(id=randint(1, 0xFFFF), seq=1))
    #p.add_header(TCPHeader(80, 80, SYN=1))
    p.set_payload('hello world')
    print(p.compile())
    print('Initializing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    print('Sending...')
    s.sendto(p.compile(), (p.get_dst(), 0))
    print('Packet sent, awaiting response...')
    print('Response:', s.recvfrom(1024))
    print('Operation complete.')
