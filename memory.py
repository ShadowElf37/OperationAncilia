class Pointer:
    def __init__(self, ram, loc, size):
        self.ram = ram
        self.loc = loc
        self.size = size

    def set(self, integer):
        d = bin(integer)[2:]
        if len(d) > self.size:
            raise MemoryError('Not enough space')
        for i in range(len(d)):
            self.ram.mem[self.loc+i] = int(d[i])

    def get(self):
        return int(''.join(map(str, self.ram.mem[self.loc:self.loc+self.size])), 2)

    def repoint(self, loc):
        self.loc = loc

    def resize(self, size):
        self.size = size

    def get_addr(self):
        return hex(self.loc)

    def get_size(self):
        return hex(self.size)

class RAM:
    def __init__(self, size):
        self.size = size
        self.mem = [None] * size

    def allocate(self, amt):
        return Pointer(self, self.mem.index(None), amt)

    def free(self, pointer):
        self.mem[pointer.loc:pointer.loc+pointer.size] = [None] * pointer.size
        del pointer