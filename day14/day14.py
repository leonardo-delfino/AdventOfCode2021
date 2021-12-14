import sys
import os
from io import BytesIO, IOBase
import numpy as np

def main():
    with open("in.txt") as f:
        data = [x for x in f.read().splitlines()]

    r = dict([l.split(" -> ") for l in data[2:]])
    x = dict(zip(r, range(len(r))))
    m = np.zeros((len(r), len(r)), dtype=object)
    for p in r:
        m[x[p[0] + r[p]]][x[p]] = 1
        m[x[r[p] + p[1]]][x[p]] = 1

    tmp = list(zip(data[0], data[0][1:]))
    c = [tmp.count((p[0], p[1])) for p in r]
    for power in [10, 40]:
        s = {data[0][0]: 1}
        for p in x:
            s[p[1]] = s.get(p[1], 0) + np.dot(np.linalg.matrix_power(m, power), c)[x[p]]
        print(s[max(s, key=lambda k: s[k])] - s[min(s, key=lambda k: s[k])])

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
