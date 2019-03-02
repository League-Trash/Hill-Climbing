import csv
import math
from random import randint
import sys

file1 = open('Boards\sudoku1.csv')

csv_reader = csv.reader(file1, delimiter=',')
sudoku_board = []
cant_change = []

# for x in range(0,-1, -1):
#     print(x)

n = 0
m = 0
for line in csv_reader:
    sudoku_board.append(line)
    for x in line:
        if int(x) != 0:
            cant_change.append([n,m])
        m += 1
    n += 1
    m = 0

#
# for line in sudoku_board:
#     print(line)

for x in range(0,len(sudoku_board)):
    for y in range(0, len(sudoku_board)):
        if int(sudoku_board[x][y]) == 0:
            sudoku_board[x][y] = randint(1,len(sudoku_board))

for line in sudoku_board:
    print(line)


def eval(s_board):
    checker = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
    errors = 0
    square_size = int(math.sqrt(len(s_board)))
    increments = []
    for x in range(0,square_size):
        increments.append((x+1)*square_size)

    for line in s_board:
        for x in line:
            num = int(x)
            if num != 0:
                if checker[num-1] > 0:
                    errors += 1
                checker[num-1] += 1
        checker = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

    for x in range(0,len(s_board)):
        for y in range(0,len(s_board)):
            num = int(s_board[y][x])
            if num != 0:
                if checker[num - 1] > 0:
                    errors += 1
                checker[num - 1] += 1
        checker = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

    low_bound = -1
    up_bound = -1

    for x in range(0,square_size):
        if x == 0:
            low_bound = 0
        else:
            low_bound = increments[x-1]
        up_bound = increments[x]
        for a in range(low_bound, up_bound):
            for b in range(low_bound, up_bound):
                num = int(s_board[a][b])
                if num != 0:
                    if checker[num - 1] > 0:
                        errors += 1
                    checker[num - 1] += 1
        checker = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

    return errors

print(eval(sudoku_board))

prevmin = sys.maxsize

while True:
    min = sys.maxsize
    changeloc = [-1,-1]
    changevar = -1
    for x in range(0,len(sudoku_board)):
        for y in range(0,len(sudoku_board)):
            OG = int(sudoku_board[x][y])
            if [x,y] not in cant_change:
                for z in range(1,len(sudoku_board)):
                    sudoku_board[x][y] = z
                    score = eval(sudoku_board)
                    if score < min:
                        min = score
                        changeloc = [x,y]
                        changevar = z
            sudoku_board[x][y] = OG
    sudoku_board[changeloc[0]][changeloc[1]] = changevar
    print(eval(sudoku_board))
    if min == prevmin:
        break
    prevmin = min



