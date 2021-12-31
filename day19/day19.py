import sys
import os
from io import BytesIO, IOBase
import re
from math import sqrt

def build_map(scanners):
    for s in scanners: distances(scanners[s])
    offsets = []
    while len(scanners) > 1:
        matches = get_matches(scanners)
        offsets.append(merge(matches, scanners))
        del scanners[matches[0]["s2"]]
        distances(scanners[matches[0]["s1"]])
    return scanners[0], offsets

def get_matches(scanners):
    matches = []
    for s1 in scanners:
        for s2 in [sx for sx in scanners if sx > s1]:
            for b1 in scanners[s1]:
                b1_ds = scanners[s1][b1]["distance"]
                for b2 in scanners[s2]:
                    b2_ds = scanners[s2][b2]["distance"]
                    if len(b1_ds.intersection(b2_ds)) >= 11:
                        matches.append(
                            {
                                "s1": s1,
                                "b1": b1,
                                "s2": s2,
                                "b2": b2
                            }
                        )
                        if len(matches) == 12:
                            return matches
    return matches

def merge(matches, scanners):
    dest = matches[0]["s1"]
    src = matches[0]["s2"]

    dest_a, dest_b, dest_diff, src_a, src_b, src_diff = [None] * 6

    n = 0
    usable = False
    while not usable:
        n += 1
        dest_a, dest_b = [scanners[dest][matches[i]["b1"]]["loc"] for i in (0, n)]
        src_a, src_b = [scanners[src][matches[i]["b2"]]["loc"] for i in (0, n)]
        dest_diff = [dest_a[i] - dest_b[i] for i in (0, 1, 2)]
        src_diff = [src_a[i] - src_b[i] for i in (0, 1, 2)]
        if len(set(dest_diff)) == 3 and len(set(src_diff)) == 3 and 0 not in src_diff and 0 not in dest_diff:
            usable = True

    src_idx = [src_diff.index(dest_diff[i]) if dest_diff[i] in src_diff
               else src_diff.index(dest_diff[i] * -1) for i in (0, 1, 2)]
    src_orientation = [dest_diff[i] / src_diff[src_idx[i]] for i in (0, 1, 2)]
    offset = [dest_a[i] - (src_a[src_idx[i]] * src_orientation[i]) for i in (0, 1, 2)]
    known_beacons = [scanners[0][i]["loc"] for i in scanners[0]]
    for b in scanners[src]:
        xformed_beacon = [int(scanners[src][b]["loc"][src_idx[i]] * src_orientation[i] + offset[i])
                          for i in (0, 1, 2)]
        if xformed_beacon not in known_beacons:
            scanners[dest][len(scanners[dest])] = {"loc": xformed_beacon}
    return offset

def distances(scanner):
    for b1 in scanner:
        x1, y1, z1 = scanner[b1]["loc"]
        scanner[b1]["distance"] = set()
        for b2 in [bx for bx in scanner if bx != b1]:
            x2, y2, z2 = scanner[b2]["loc"]
            distance = sqrt((x1-x2) ** 2 + (y1-y2) ** 2 + (z1-z2) ** 2)
            scanner[b1]["distance"].add(distance)

def find_longest_distance(offsets):
    m = 0
    for i in range(len(offsets)):
        for j in range(i + 1, len(offsets)):
            n = sum([abs(offsets[i][k] - offsets[j][k]) for k in (0, 1, 2)])
            m = n if n > m else m
    return int(m)

def main():
    data = {}
    scanner = None
    with open("in.txt") as f:
        for line in f:
            if line.startswith("--- scanner "):
                scanner = int(re.search(r'\d+', line).group())
                data[scanner], c = {}, 0
            elif line.strip():
                data[scanner][c] = {"loc": [int(i) for i in line.split(',')]}
                c += 1
    b, off = build_map(data)

    # part 1
    print(len(b))
    # part 2
    print(find_longest_distance(off))

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
