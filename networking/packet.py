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
        self.ip_len_recalc()

    def set_payload(self, s):
        self.payload = s
        self.ip_len_recalc()

    def ip_len_recalc(self):
        if isinstance(self.headers[0], IPHeader):
            # print(self.headers[0].header)
            t = 0
            for h in self.headers:
                t += len(h.compile())
            t += len(self.payload)
            self.headers[0].header[2] = t

    def compile(self):
        return b''.join([p.compile() for p in self.headers]) + self.payload.encode(ENC)

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dest


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
        b = int(n, 2)
        if debug: print(5, b)
        self.header[-3] = b

        return pack('!BBHHHBBH4s4s', *self.header)


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
        b = int(n, 2)
        if debug: print(5, n)
        self.header[2] = b
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


class UDPHeader:
    def __init__(self):
        ...


class NATHeader:
    def __init__(self):
        ...

if __name__ == '__main__':
    print('Initializing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    src = '192.168.1.81'
    dst = '192.168.1.164'
    payload = 'test'
    print('Socket ready. Creating packets...')

    for i in range(3):
        p = Packet(dst)
        p.add_header(IPHeader(src, dst, protocol=protocols.ICMP))
        p.add_header(ICMPHeader(payload, type=8, seq=i))
        #p.add_header(TCPHeader(80, 80, SYN=1))
        p.set_payload(payload)
        #print(p.compile())
        # print(p.headers[0].header)
        s.sendto(p.compile(), ('192.168.1.1', 0))
        print('ICMP Echo request sent.')
        print('Response:', s.recvfrom(1024))

    print('Operation complete.')
