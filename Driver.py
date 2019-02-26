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
 
#Used to find the positions of queens on the board and append them to a list.
#Simple way to work with only the queens positions for the queenHeuristic
def indices():
  global tempBoard
  for i in range(len(tempBoard)):
    for j in range(len(tempBoard[i])):
      if tempBoard[i][j] == 1:
        indexList.append([i,j])

#A heurstic funtion to return the number of conflicts a queen has with other queens on the board.
#Queens with more conflicts are considered first when attempting a move. INCOMPLETE
def queenHeuristic(lst):
  conflicts = 0
  currentCheck = 0
  for i in range(len(lst)):
    currentCheck = lst[i]
    for j in range(len(lst)):
      if currentCheck == lst[j]:
        continue
      elif currentCheck[0] == lst[j][0]:
        conflicts = conflicts + 1
      elif currentCheck[1] == lst[j][1]:
        conflicts = conflicts + 1
      elif abs(currentCheck[0] - lst[j][0]) == abs(currentCheck[1] - lst[j][1]):
        conflicts = conflicts + 1


#def hillClimbing(lst):
    

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

queenHeuristic(indexList)
