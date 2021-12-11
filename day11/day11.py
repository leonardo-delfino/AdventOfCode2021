import sys
import os
from io import BytesIO, IOBase

c = [-1, 1, -1j, 1j, -1 - 1j, -1 + 1j, 1 + 1j, 1 - 1j]

def flash(grid, p):
    grid[p] = 0
    for value in c:
        tmp = p + value
        if tmp in grid and grid[tmp] > 0:
            grid[tmp] += 1
    return 1

def step(grid):
    for p in grid:
        grid[p] += 1
    s = 0
    while flashes := sum(flash(grid, p) for p, v in grid.items() if v > 9):
        s += flashes
    return s

def main():
    grid = {x + y * 1j: int(c) for x, line in enumerate(open("in.txt")) for y, c in enumerate(line.strip())}
    steps = 100

    # part 1
    print(sum(step(grid) for _ in range(steps)))

    # part 2
    while step(grid) != 100: steps += 1
    print(steps + 1)

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
