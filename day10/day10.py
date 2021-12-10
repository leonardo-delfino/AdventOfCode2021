import sys
import os
from io import BytesIO, IOBase
from statistics import median

def main():
    with open("in.txt") as f:
        data = [line.strip() for line in f]

    error = 0
    res = []
    for line in data:
        prompt = ""
        for char in line:
            if char in "([{<":
                prompt += char
            elif prompt[-1] == {")": "(", "]": "[", "}": "{", ">": "<"}[char]:
                prompt = prompt[:-1]
            else:
                error += {")": 3, "]": 57, "}": 1197, ">": 25137}[char]
                break
        else:
            res.append(prompt)

    # part 1
    print(error)

    # part 2
    scores = [0] * len(res)
    for i, s in enumerate(res):
        for char in s[::-1]:
            scores[i] = (scores[i] * 5) + {"(": 1, "[": 2, "{": 3, "<": 4}[char]
    print(median(scores))

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
