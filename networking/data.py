import socket
from time import sleep

class Bin:
    def __init__(self, value, length=8):
        self.value = value
        self.length = length
        self.value = int('0' * (len(bin(self.value))-2) + bin(self.value)[2:], 2)

    def __add__(self, other):
        if not isinstance(other, Bin):
            raise TypeError('Cannot add two non-Bin structures')

        self.value <<= other.length
        self.value += other.value
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return 'Bin with value ' + str(self.value)

def cut(s, interval):
    t = []
    i = 1
    d = ''
    s = reversed(s)
    for c in s:
        d += c
        if i == interval:
            t.append(d)
            d = ''
            i = 1
            continue
        i += 1
    if d:
        t.append(d)

    t = list(reversed([''.join(list(reversed(i))) for i in t]))
    return t

def hexpad(ints, sizes):
    return ''.join([('0' * (sizes[i] - len(hex(ints[i])[2:])) + hex(ints[i])[2:]) for i in range(len(ints))])

def binsum(hex):
    return bin(sum(list(map(lambda x: int(x, 16), hex))))[2:]

def carry(b, l=4):
    while len(b) > l:
        b = bin(int(b[0], 2) + int(''.join(b[1:]), 2))[2:]
        b = '0' * (len(b) % 4) + b
        b = cut('0' * (len(b) % 4) + b, 4)

    return b

def onecomplement(string):
    n = ''
    for c in string:
        if c == '1':
            n += '0'
        else:
            n += '1'

    return n