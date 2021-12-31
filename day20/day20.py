import sys
import os
from io import BytesIO, IOBase
import pandas as pd
import numpy as np
from scipy.ndimage import generic_filter

def main():
    raw_data = pd.read_csv("in.txt")
    data = raw_data.iloc[:, 0].str.split("", expand=True).iloc[:, 1:-1].replace({"#": 1, ".": 0}).astype(np.uint16).to_numpy()
    s = np.where(np.array(list(raw_data.columns[0])) == "#", True, False).astype(np.uint16)
    footprint = np.ones((3, 3))
    it = 50
    sums = []
    for i in range(it):
        data = generic_filter(
            input=np.pad(data, 1, "constant", constant_values=((i % 2) if s[0] == True else 0)),
            function=lambda m: s[np.sum(m*np.array([256, 128, 64, 32, 16, 8, 4, 2, 1]).astype(np.uint16), dtype=np.uint16)],
            footprint=footprint,
            mode="nearest"
        )
        sums.append(data.sum())

    # part 1
    print(sums[1])

    # part 2
    print(sums[it-1])

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
