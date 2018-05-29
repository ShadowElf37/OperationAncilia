import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('192.168.1.164', 37377))

print('Socket listening...')
while True:
    print('Packet received:', s.recvfrom(1024))