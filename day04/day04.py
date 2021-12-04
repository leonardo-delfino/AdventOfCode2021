import os
import sys
from io import BytesIO, IOBase

BOARD_SIZE = 5

def mark_board(board, draw):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == draw:
                board[i][j] = None

def check_boards(boards, winning_boards):
    for i, board in enumerate(boards):
        if i in winning_boards:
            continue
        if check_rows_columns(board):
            return i
    return None

def check_rows_columns(board):
    for i in range(BOARD_SIZE):
        r, c = 1, 1
        for j in range(BOARD_SIZE):
            if board[i][j] is not None:
                r = 0
            if board[j][i] is not None:
                c = 0
            if not r and not c:
                break
        if r or c:
            return 1
    return 0

def calculate_sum(board, draw):
    s = 0
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value is not None:
                s += value
    return s*draw

def main():
    with open("in.txt") as f:
        numbers = list(map(int, f.readline().strip().split(","))); f.readline()
        table = [[[int(num) for num in row.split()] for row in board.split("\n")] for board in f.read().split("\n\n")]

    boards = []
    s = 0
    for draw in numbers:
        for i, board in enumerate(table):
            if i not in boards:
                mark_board(board, draw)
        b = 0
        while b is not None:
            b = check_boards(table, boards)
            if b is not None and b not in boards:
                boards.append(b)
                s = calculate_sum(table[b], draw)
                if len(boards) == 1:
                    print(s)
    print(s)

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
