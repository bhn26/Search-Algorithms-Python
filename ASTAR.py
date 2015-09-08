from Queue import *
from heapq import *
from copy import *

#is_complete runs through the board and checks to see if the elements
#are in increasing order, if not, return false, otherwise, return true.
def is_complete(board):
	tmp = 0
	for x in board:
		for y in x:
			if tmp != y:
				return False
			else:
				tmp = tmp + 1
	return True

#is_valid runs through the board to make sure it has every number
#from 0 to NxM-1 in order to see if it is valid to solve in the
#first place.
def is_valid(board):
	elmt = []

	for x in board:
		for y in x:
			elmt.append(y)
	
	elmt.sort()

	for i in range(len(elmt)):
		if i != elmt[i]:
			return False
	
	return True

#make_move simply switchs two spots on a board with each other.
#Parameters are the board, the x,y coords of the first spot
#and then the x,y coords of the second
def make_move(board, x1,y1,x2,y2):
	old = -1
	new = -1
	dx = 0
	dy = 0
	for x in board:
		for y in x:
			if (dx == x1 and dy == y1):
				old = y
			elif (dx == x2 and dy == y2):
				new = y
			dy = dy + 1
		dx = dx + 1
		dy = 0
	board[x2][y2] = old
	board[x1][y1] = new
	return board

#state_space turns the board into a string in order then hashes it to
#make a unique value to put into the visited list
def state_space(board):
	state = ""
	for x in board:
		for y in x:
			state += str(y)
	return hash(state)

#poszero finds the position of the zero piece on the board and returns it
def poszero(board):
	tmp = [-1,-1]
	dx = 0
	dy = 0
	for x in board:
		for y in x:
			if (y == 0):
				tmp[0] = dx
				tmp[1] = dy
			dy = dy + 1
		dy = 0
		dx = dx + 1
	return tmp

#heuristic takes in a state of the board and the solved state then
#calculates the difference from each piece of the current state with
#the goal state and returns the heuristic score.
def heuristic(state, solved):
	value = 0

	width = len(state)
	length = len(state[0])

	cords = {}

	for x in range(width):
		for y in range(length):
			cords[state[x][y]] = (x,y)

	width = len(solved)
	length = len(solved[0])

	for x in range(width):
		for y in range(length):
			tmp = solved[x][y]
			(tmpx,tmpy) = cords[tmp]

			value += abs(tmpx - x)
			value += abs(tmpy - y)
	
	return value

#A_STAR takes in a list representation of the board and runs a A*
#search algorithm on it
def A_STAR(board):
	
	#Stores the initial copy of the board
	start = deepcopy(board)

	#Find the width and length of the board
	width = len(board)
	length = len(board[0])

	#Priorities of the directions if a tie happens
	UP = 4
	DP = 3
	LP = 2
	RP = 1

	#Create a solved board with the same dimesnions as input
	h_checker = []
	i = 0
	for x in range(width):
		xs = []
		for y in range(length):
			xs.append(i)
			i = i + 1
		h_checker.append(xs)

	#Checks the heuristic value
	heur = heuristic(start,h_checker)

	#Initialize heap and push pair containing travel path and state
	q = []
	heappush(q, (heur, 0, [], start, 0))

	#Initialize visited list and adds the initial
	visited = []

	#Runs the A_STAR while heap is not empty
	while (len(q)):
		
		#Gets the item in front of the heap
		(pri, prix, trav, tmp_state, depth) = heappop(q)
		
		#Checks if the state is complete, if so, print traverse path
		#then return
		if (is_complete(tmp_state)):
			print ("".join(trav))
			return

		#Otherwise expand the heap witht he neighbors
		else:
			#Makes copy of the state and adds it to visited list
			new_state = deepcopy(tmp_state)
			visited.append(state_space(new_state))
		
			#Grabs the position of 0
			zpos = poszero(new_state)

			#Flags to see if the move is possible
			U = 0
			D = 0
			R = 0
			L = 0
			
			#Checks if moves are possible then changes flags
			if (zpos[0] - 1 != -1 ):
				U = 1
			if (zpos[0] + 1 != width ):
				D = 1
			if (zpos[1] - 1 != -1 ):
				L = 1
			if (zpos[1] + 1 != length ):
				R = 1

			#Checks each flag and then makes the move.
			#It then checks if the board is already in the visited
			#list, if not, then it appends the path traveled to 
			#traverse. It then increments the depth value and then 
			#comes up with the new heuristic value. Afterwards, it 
			#pushes the new values onto the heap. It does this for 
			#the other three directions too.
			if(U == 1):
				moved_state = deepcopy(new_state)
				moved_state = make_move(moved_state, zpos[0], zpos[1], zpos[0]-1, zpos[1])

				if state_space(moved_state) not in visited:
					new_traverse = list(trav) + ["U"]
					tmpdepth = depth + 1
					value = tmpdepth + heuristic(moved_state, h_checker)
					priy = UP
					heappush(q, (value, priy, list(new_traverse), moved_state, tmpdepth))
			if(D == 1):
				moved_state = deepcopy(new_state)
				moved_state = make_move(moved_state, zpos[0], zpos[1], zpos[0]+1, zpos[1])

				if state_space(moved_state) not in visited:
					new_traverse = list(trav) + ["D"]
					tmpdepth = depth + 1
					value = tmpdepth + heuristic(moved_state, h_checker)
					priy = DP
					heappush(q, (value, priy, list(new_traverse), moved_state, tmpdepth))
			if(L == 1):
				moved_state = deepcopy(new_state)
				moved_state = make_move(moved_state, zpos[0], zpos[1], zpos[0], zpos[1]-1)

				if state_space(moved_state) not in visited:
					new_traverse = list(trav) + ["L"]
					tmpdepth = depth + 1
					value = tmpdepth + heuristic(moved_state, h_checker)
					priy = LP
					heappush(q, (value, priy, list(new_traverse), moved_state, tmpdepth))
			if(R == 1):
				moved_state = deepcopy(new_state)
				moved_state = make_move(moved_state, zpos[0], zpos[1], zpos[0], zpos[1]+1)

				if state_space(moved_state) not in visited:
					new_traverse = list(trav) + ["R"]
					tmpdepth = depth + 1
					value = tmpdepth + heuristic(moved_state, h_checker)
					priy = RP
					heappush(q, (value, priy, list(new_traverse), moved_state, tmpdepth))

	#Prints "UNSOLVABLE" and returns if no solution
	print ("UNSOLVABLE")
	return

def main():
	import sys
	board=[[int(n.strip()) for n in line.split(",")] for line in sys.stdin.readlines()]
	
	#Checks if the board is valid to run alg on, if not, 
	#print "UNSOLVABLE" and return
	if not is_valid(board):
		print ("UNSOLVABLE")
		return
	
	#Checks if board is already complete, otherwise run alg
	if is_complete(board):
		print ("")
	else:
		A_STAR(board)

if __name__ == "__main__":
	main()
