import sys
import os
from io import BytesIO, IOBase
import functools
import itertools

def part_1(p1, s1, p2, s2):
    end = r = 0
    while True:
        end = end % 100 + 1
        if end % 2:
            p1 += sum([end, end+1, end+2])
            s1 += p1 % 10 if p1 % 10 else 10
        else:
            p2 += sum([end, end+1, end+2])
            s2 += p2 % 10 if p2 % 10 else 10
        end += 2
        r += 3
        if s1 >= 1000 or s2 >= 1000:
            break
    return s1, s2, r

# vvv this is so cool
@functools.lru_cache(maxsize=None)
def play_out(p1, s1, p2, s2):
    w1 = w2 = 0
    for m1, m2, m3 in itertools.product((1, 2, 3), (1, 2, 3), (1, 2, 3)):
        p1_c = (p1+m1+m2+m3) % 10 if (p1+m1+m2+m3) % 10 else 10
        s1_c = s1 + p1_c
        if s1_c >= 21:
            w1 += 1
        else:
            w2_c, w1_c = play_out(p2, s2, p1_c, s1_c)
            w1 += w1_c
            w2 += w2_c
    return w1, w2

def main():
    with open("in.txt") as f:
        data = f.read().strip().split('\n')
    s1, s2, r = part_1(int(data[0][-1]), 0, int(data[1][-1]), 0)

    # part 1
    print(min(s1, s2) * r)

    # part 2
    print(max(play_out(int(data[0][-1]), 0, int(data[1][-1]), 0)))

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
