#Sinclair Fuh, Zachary Taylor, Thomas Cooper
#COSC 370, Artificial Intelligence

#====================
#
#      Imports      
#
#====================
import csv
import math
import random
import sys
import os

#====================
#
#  Global Variables
#
#====================
queenBoard = []
indexList = []
originalIndexList = []
sudoku_board = []
cant_change = []
verbose = 2

#====================
#
#  Helper Functions
#
#====================

#
#  Creates a 2d chessboard and populates the board with queens.
#  Gives the array n queens and ((n*n)-n) empty spaces and shuffles them.
#  Then every n spots, it creates a new entry in the array and appends
#  a list of all elements up to n.
#
def createBoard(n):
	global queenBoard
	queenBoard = ([1] * n) + ([0] * ((n*n) - n))
	random.shuffle(queenBoard)
	queenBoard = [queenBoard[i:i+n] for i in range(0, n*n, n)]

#
#  Creates an list of indexes of queen positions for use with the
#  queenHeuristic function. 
#
def indices():
	global queenBoard
	for i in range(len(queenBoard)):
		for j in range(len(queenBoard[i])):
			if queenBoard[i][j] == 1:
				indexList.append([i,j])

#
#  Evaluation function for n-Queens problem.
#  Checks the board for conflicts by using indexList. Checks
#  if it's comparing againt itself to not add conflicts for where it is
#  currently standing. Checks column and row for conflicts as well as checking
#  diagonals for conflicts. Doing this collects the conflict state for the entire
#  chessboard.
#
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

#
#  evaluation function for Sudoku board.
#  Uses the checker array to store numbers from the 
#  current row/column/5x5 square. If a number is encountered
#  twice in this array, it increases the number of errors.
#  Total error number is the amount of conflicts on the board.
#
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

#
#  Simulated annealing code for Sudoku. Takes a map (starting board) and a 
#  number of iterations to go through. It uses random chance to determine whether
#  to continue hill-climbing or to make a potentially bad move to try to approach
#  a global maximum rather than a local maximum.
#
def sim_annealing(map, max_iters):
	print("\n\nSimulated Annealing for Sudoku beginning: ")
	print("\nStarting board state: ")
	for line in map:
		print(line)
	possible_nums = []
	for i in range(0,len(map)):
		possible_nums.append(i+1)

	for i in range(0,max_iters):
		changex = random.randint(0,len(map)-1)
		changey = random.randint(0, len(map)-1)
		while [changex, changey] in cant_change:
			changex = random.randint(0, len(map)-1)
			changey = random.randint(0, len(map)-1)

		prevnum = map[changex][changey]
		possible_nums.remove(prevnum)
		changevar = possible_nums[random.randint(0,len(possible_nums)-1)]
		possible_nums.append(prevnum)

		preveval = eval(map)

		map[changex][changey] = changevar

		posteval = eval(map)

		if (posteval <= preveval):
			map = map
		elif ((i/max_iters) + (posteval-preveval)*0.4) < random.uniform(0,0.9):
			map[changex][changey] = prevnum

		if verbose == 1:
			print("\nCurrent Board state:")
			for line in map:
				print(line)
		print("Current error score (lower is better): ", eval(map))

#===================
#
#     Main Code
#
#===================

#Select the problem to solve, and whether you want verbose output or not.

selection = int(input("Which problem would you like to attempt?\n1.) n-Queens\n2.) Sudoku the Giant "))
verbose = int(input("Would you like verbose output?\n1.) Yes\n2.) No "))

#n-Queens problem
if selection == 1:
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

#Sudoku The Giant Problem
elif selection == 2:
	#User input for file name
	filename = input("Enter a sudoku board csv filename: ")
	
	#Check to see if file exists
	if os.path.exists(filename):
		file1 = open(filename)	
		csv_reader = csv.reader(file1, delimiter=',')
	else:
		print("File not found, closing.")
	
	n = 0
	m = 0
	
	#Creates the sudoku board from the csv file
	for line in csv_reader:
		sudoku_board.append(line)
		for x in line:
			if int(x) != 0:
				cant_change.append([n,m])
			m += 1
		n += 1
		m = 0

	#If there is no number on the sudoku board, insert a random number. Creates a starting state.
	for x in range(0,len(sudoku_board)):	
		for y in range(0, len(sudoku_board)):
			if int(sudoku_board[x][y]) == 0:
				sudoku_board[x][y] = random.randint(1,len(sudoku_board))

	print("\nStarting Sudoku Board: ")
	for line in sudoku_board:
		print(line)

	#Hill-Climbing begins here
	prevmin = sys.maxsize

	while True:
		#Create variables for algorithm
		min = sys.maxsize
		changeloc = [-1,-1]
		changevar = -1

		for x in range(0,len(sudoku_board)):
			for y in range(0,len(sudoku_board)):
				#Create copy of current position to replace later
				OG = int(sudoku_board[x][y])
				#if [x,y] is not a number already provided
				if [x,y] not in cant_change:
					for z in range(1,len(sudoku_board)):
						#Try every number 1 to len(sudoku_board) and eval to check new score
						sudoku_board[x][y] = z
						score = eval(sudoku_board)
						#if score is a new best then update the best score, and make the change to the board space.
						if score < min:
							min = score
							changeloc = [x,y]
							changevar = z
				#reset the board back to it's previous state
				sudoku_board[x][y] = OG
		#change the board tile to the new best
		sudoku_board[changeloc[0]][changeloc[1]] = changevar
	
		print("\nCurrent conflict score (lower is better):",eval(sudoku_board))
		if verbose == 1:
			print("Current board state: ")		
			for line in sudoku_board:
				print(line)
		if min == prevmin:
			print("Final conflict score (lower is better):", eval(sudoku_board))		
			break
		prevmin = min	
	
	sim_annealing(sudoku_board, 1000000)


