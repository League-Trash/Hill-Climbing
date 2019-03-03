#Sinclair Fuh, Zachary Taylor, Thomas Cooper
#COSC 370, Artificial Intelligence

import random
import sys
queenBoard = []
indexList = []
originalIndexList = []

#sets up a 1d array of queen positions.
def createBoard(n):
	global queenBoard
	queenBoard = ([1] * n) + ([0] * ((n*n) - n))
	random.shuffle(queenBoard)
	queenBoard = [queenBoard[i:i+n] for i in range(0, n*n, n)]

def indices():
	global queenBoard
	for i in range(len(queenBoard)):
		for j in range(len(queenBoard[i])):
			if queenBoard[i][j] == 1:
				indexList.append([i,j])

#Checks whole board for conflicts with queens to return the value of all conflicts on the board.
def queenHeuristic(lst):
	#print(lst)
	conflicts = 0
	currentCheck = 0
	for i in range(len(lst)):
		currentCheck = lst[i]
		for j in range(len(lst)):
			if currentCheck == lst[j]:
				continue
			elif currentCheck[0] == lst[j][0]:
				conflicts += 1
			elif currentCheck[1] == lst[j][1]:
				conflicts += 1
			elif abs(currentCheck[0] - lst[j][0]) == abs(currentCheck[1] - lst[j][1]):
				conflicts += 1
	return conflicts
#Main program begins here

size = int(input("Choose a number of queens to solve for: "))
if size <= 250:
	#create a board
	changed = False
	createBoard(size)
	#copy the board to an operating board to preserve original for annealing
	opBoard = queenBoard[:]
	#find positions of all queens to use for heuristic
	indices()
	print("starting board, ", opBoard)
	prevmin = sys.maxsize
	while True:
		#initialize variables
		min = sys.maxsize
		changeloc = [-1,-1]
		changevar = -1
		#select queen to move
		for queen in indexList:
			opBoard[queen[0]][queen[1]] = 0
			#for x position
			for x in range(len(opBoard)):
				#for y position
				for y in range(len(opBoard)):
					ogBoard = opBoard[:]
					#set the current queen position to 0 to remove her from the board and prepare to move her
					if opBoard[x][y] == 0:
						opBoard[x][y] = 1
						changed = True
					print(opBoard)
					originalIndexList = indexList[:]
					indices()
					score = queenHeuristic(indexList)
					if score < min:
						min = score
						changeloc = [x,y]
					if changed:
						opBoard[x][y] = 0
						changed = False
					indexList = originalIndexList[:]				
					opBoard = ogBoard[:]
					opBoard[changeloc[0]][changeloc[1]] = 1
			for line in opBoard:
				print(line)
			print("score, ", queenHeuristic(indexList))
			indexList = originalIndexList[:]
			if min == prevmin:
				break
			prevmin = min


