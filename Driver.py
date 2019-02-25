#Sinclair Fuh, Zachary Taylor, Lron Coop
#COSC 370, Artificial Intelligence

import random

queenBoard = []
indexList = []
tempBoard = []

#Some help from https://stackoverflow.com/questions/33811240/python-randomly-fill-2d-array-with-set-number-of-1s
#To help with randomly populating th board efficiently. queenBoard[i:i+n] fills in the next n spots
#with the next n positions from the 1d array, then makes a new index and inserts the next n. Doing this
#helps convert the shuffled 1d array into a shuffled 2d array
def createBoard(n):
  global queenBoard
  queenBoard = ([1] * n) + ([0] * ((n*n) - n))
  random.shuffle(queenBoard)
  queenBoard = [queenBoard[i:i+n] for i in range(0, n*n, n)]
  
def indices():
  global tempBoard
  for i in range(len(tempBoard)):
    for j in range(len(tempBoard[i])):
      if tempBoard[i][j] == 1:
        indexList.append([i,j])

def hillClimbing(lst):
    

#Main program begins here
print("1.) n-Queens\n2.) Sudoku the Giant")
selection = int(input("Choose a Problem to solve: "))

if selection == 1:
  size = int(input("Choose a number of queens to solve for: "))
  createBoard(size)
  tempBoard = queenBoard
  indices()

print(queenBoard)
print(indexList)
