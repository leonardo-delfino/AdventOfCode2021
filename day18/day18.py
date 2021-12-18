import sys
import os
from io import BytesIO, IOBase
import math
import itertools
from functools import reduce

def add_left(n, num):
    return (n + num) if isinstance(n, int) else ([add_left(n[0], num), n[1]])

def add_right(n, num):
    return (n + num) if isinstance(n, int) else ([n[0], add_right(n[1], num)])

def _add(l):
    while True:
        exploded, _, l, _ = explode(l)
        if exploded:
            continue
        exploded, l = split(l)
        if not exploded:
            break
    return l

def add(n, m):
    return _add([n, m])

def split(num):
    if isinstance(num, int):
        return (True, [num // 2, math.ceil(num / 2)]) if num >= 10 else (False, num)
    n, m = num
    s, n = split(n)
    if s:
        return True, [n, m]
    s, m = split(m)
    return s, [n, m]

def explode(num, d=4):
    if isinstance(num, int): return False, 0, num, 0
    if d == 0: return True, num[0], 0, num[1]
    n, m = num
    exploded, l, n, r = explode(n, d - 1)
    if exploded:
        return True, l, [n, add_left(m, r)], 0
    exploded, l, m, r = explode(m, d - 1)
    return (True, 0, [add_right(n, l), m], r) if exploded else (False, 0, num, 0)

def magnitude(num):
    if isinstance(num, int):
        return num
    return 3*magnitude(num[0]) + 2*magnitude(num[1])

def main():
    with open("in.txt") as f:
        data = [eval(line) for line in f.read().splitlines()]

    print(magnitude(reduce(add, data)))
    print(max(magnitude(add(a, b)) for a, b in itertools.permutations(data, 2)))

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
