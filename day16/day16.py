import sys
import os
from io import BytesIO, IOBase
from math import prod

OPERATIONS = {
    0: sum, 1: prod, 2: min, 3: max,
    5: lambda x: int(x[0] > x[1]),
    6: lambda x: int(x[0] < x[1]),
    7: lambda x: int(x[0] == x[1])
}

def parse_data(data):
    ptr = 0
    res = []
    while True:
        res.append(data[ptr + 1:ptr + 5])
        if data[ptr] == "0":
            break
        ptr += 5
    return 5 * len(res), int("".join(res), base=2)

def parse_packet(data):
    v = int(data[:3], base=2)
    id = int(data[3:6], base=2)
    s = 6
    if id == 4:
        p, n = parse_data(data[s:])
        return v, n, s+p

    r = v
    nn = []
    if data[s] == "0":
        subp, s = int(data[s+1:s+16], base=2), s + 16
        parse = s + subp
        while s < parse:
            v, n, p = parse_packet(data[s:])
            s += p
            r += v
            nn.append(n)
    else:
        c_subp = int(data[s+1:s+12], base=2)
        s += 12
        for _ in range(c_subp):
            v, n, p = parse_packet(data[s:])
            s += p
            r += v
            nn.append(n)
    return r, OPERATIONS[id](nn), s

def main():
    sol = parse_packet("".join(f"{int(x, 16):04b}" for x in open("in.txt").read().strip()))
    # part 1
    print(sol[0])
    # part 2
    print(sol[1])

# region fastio

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# endregion

if __name__ == "__main__":
    main()
