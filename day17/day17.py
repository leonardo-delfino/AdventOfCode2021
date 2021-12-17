import sys
import os
from io import BytesIO, IOBase
from re import findall
from math import sqrt

def valid(v, x, y):
    v0 = [0, 0]
    while True:
        for i in range(2):
            v0[i] += v[i]
        if v[0]: v[0] -= 1
        v[1] -= 1
        if x[0] <= v0[0] <= x[1] and y[0] <= v0[1] <= y[1]:
            return True
        if v0[0] > x[1] or v0[1] < y[0]:
            return False

def main():
    with open("in.txt") as f:
        data = list(map(int, findall("-?\d+", f.read().strip())))
    x = (data[0], data[1])
    y = (data[2], data[3])
    v = (
        (int(sqrt(x[0]*2)), y[0]),
        (x[1], abs(y[0]+1))
    )

    # part 1
    print((v[1][1]+1) * v[1][1]//2)

    part_2 = 0
    for v_x in range(v[0][0], v[1][0]+1):
        for v_y in range(v[0][1], v[1][1]+1):
            part_2 += valid([v_x, v_y], x, y)

    # part 2
    print(part_2)

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
