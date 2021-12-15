import sys
import os
from io import BytesIO, IOBase
import heapq

def dijkstra(graph):
    r, c = len(graph), len(graph[0])
    costs = {}
    heap = [(0, 0, 0)]
    while heap:
        cost, i, j = heapq.heappop(heap)
        if (i, j) == (r - 1, c - 1):
            return cost
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < r and 0 <= nj < c:
                ncost = cost + graph[ni][nj]
                if costs.get((ni, nj), float('inf')) <= ncost:
                    continue
                costs[(ni, nj)] = ncost
                heapq.heappush(heap, (ncost, ni, nj))

def main():
    with open("in.txt", ) as f:
        data = [list(map(int, line)) for line in f.read().split('\n')]

    rows, cols = len(data), len(data[0])
    er, ec = len(data) * 5, len(data[0]) * 5
    extension = [[0 for _ in range(ec)] for _ in range(er)]
    for i in range(er):
        for j in range(ec):
            dist = i // rows + j // cols
            current = data[i % rows][j % cols] + dist
            current = current % 9 or current
            extension[i][j] = current

    # part 1
    print(dijkstra(data))

    # part 2
    print(dijkstra(extension))

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
