import os
import sys
from io import BytesIO, IOBase

# recursive because why not
def rating(data, position, bit="0"):
    if len(data) == 1:
        return data
    position %= len(data[0])
    bits_p = [line[position] for line in data]
    return rating(
        [line for line in data if line[position] == (
            bit if bits_p.count("1") >= bits_p.count("0") else list({"0", "1"}.difference({bit}))[0]
        )], position + 1, bit
    )

def main():
    with open("in.txt") as f:
        data = [line for line in f]

    # part 1
    gamma_bits = ["1" if p.count("1") > p.count("0") else "0" for p in zip(*data)]
    gamma = int("".join(gamma_bits), 2)
    epsilon = gamma ^ int("1"*(len(data[0])-1), 2)
    print(gamma*epsilon)

    # part 2
    oxygen = int(rating(data, 0, "1")[0], 2)
    co2 = int(rating(data, 0)[0], 2)
    print(oxygen*co2)

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
