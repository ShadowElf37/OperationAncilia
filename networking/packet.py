import socket
from random import randint
from struct import pack
import header.data as data
import protocols
import header.level2 as level2, header.level3 as level3, header.level4 as level4

class Packet:
    def __init__(self, dest, src=socket.gethostbyname(socket.gethostname())):
        self.l2 = None
        self.l3 = None
        self.l4 = None
        self.datagram = ''
        self.dest = dest
        self.src = src

    def add_header(self, a):
        self.headers.append(a)

    def set_datagram(self, s):
        self.datagram = s

    def ip_len_recalc(self):
        if isinstance(self.l3, level3.IPHeader):
            # print(self.headers[0].header)
            t = 0
            for h in [h for h in [self.l2, self.l3, self.l4] if h is not None]:
                t += len(h.compile())
            t += len(self.datagram)
            self.l3.header[2] = t

    def compile(self):
        self.ip_len_recalc()
        return b''.join([p.compile() for p in [self.l2, self.l3, self.l4] if p is not None]) + self.datagram.encode(data.ENC)

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dest


if __name__ == '__main__':
    print('Initializing socket...')
    # s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    # s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.bind(('eth0', 0))

    print('Socket ready. Sending packet...')
    src = '192.168.1.1'
    dst = '192.168.1.81'
    smac = 'AC:9E:17:7D:2E:80' # 'b0:65:bd:45:c9:c8'
    dmac = '7c:d1:c3:71:1c:86'
    payload = 'This packet has massive spoof lol got em'

    for i in range(1):
        p = Packet(dst)
        p.l2 = level2.MACHeader(smac, dmac, protocols.E_ARP)
        p.l3 = level2.ARPHeader(src, smac, dst, protocols.E_IPv4)
        # p.l4 = level3.IPHeader(src, dst, protocol=protocols.UDP)
        # p.l4 = level4.ICMPHeader(payload, type=8, seq=1)
        # p.l4 = level4.TCPHeader(payload, src, dst, 37377, 37377, SYN=1)
        # p.l4 = level4.UDPHeader(payload, 37377)
        p.set_datagram(payload)

        print(p.compile())
        s.send(p.compile())
        print('ARP packet sent.')
        print('Response:', s.recvfrom(1024))

    print('Operation complete.')
