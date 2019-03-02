#Sinclair Fuh, Zachary Taylor, Thomas Cooper
#COSC 370, Artificial Intelligence

import random

queenBoard = []
board = []
tempBoard = []

#sets up a 1d array of queen positions.
def createBoard(n):
  global queenBoard
  for i in range(n):
    queenBoard.append(i)
  random.shuffle(queenBoard)


#Checks whole board for conflicts with queens to return the value of all conflicts on the board.
def queenHeuristic(board):
  conflicts = 0
  for i in board:
    for j in board:
      if board[i] == board[j]:
        conflicts += 1
      elif abs(j - i) == abs(board[j] - board[i]):
        conflicts += 1
  return conflicts
  
#Main program begins here
print("1.) n-Queens\n2.) Sudoku the Giant")
selection = int(input("Choose a Problem to solve: "))

if selection == 1:
  size = int(input("Choose a number of queens to solve for: "))
  if size <= 250:
    createBoard(size)
    board = queenBoard
    for i in range(50000):
      bestVal = queenHeuristic(board)
      for j in range(len(board)):
        tempBoard = board
        for k in range(len(board)):
          tempBoard[j] = k
          currentVal = queenHeuristic(tempBoard)
          if currentVal < val:
            
print(queenBoard)
