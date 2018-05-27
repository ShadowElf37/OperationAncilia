class Bin:
    def __init__(self, value, length=8):
        self.value = value
        self.length = length
        self.value <<= length-(len(bin(self.value))-2)

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