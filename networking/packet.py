import socket
from random import randint
from struct import pack
import header.data as data
import protocols
import header.level2 as level2, header.level3 as level3, header.level4 as level4

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
        if isinstance(self.headers[0], level3.IPHeader):
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


if __name__ == '__main__':
    print('Initializing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    src = '192.168.1.164'
    dst = '192.168.1.81'
    payload = 'test'
    print('Socket ready. Entering loop...')

    for i in range(3):
        p = Packet(dst)
        p.add_header(level3.IPHeader(src, dst, protocol=protocols.ICMP))
        p.add_header(level4.ICMPHeader(payload, type=8, seq=i))
        #p.add_header(header.level4.TCPHeader(80, 80, SYN=1))
        p.set_payload(payload)
        #print(p.compile())
        # print(p.headers[0].header)
        s.sendto(p.compile(), ('192.168.1.81', 0))
        print('ICMP Echo request sent!')
        print('Response:', s.recvfrom(1024))

    print('Operation complete.')
