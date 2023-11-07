import random 
import copy

A = [['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.']]
scores = {}

vs_computer = False; dif_level = "NONE"

def read_file():
	try:
		f = open("scoreboard.txt", "r")
	except:
		f = open("scoreboard.txt", "w")
		f.close()
		return
	for s in f:
		name = ''; scor = ''; i =0
		while i < len(s):
			if s[i] != ' ':
				name += s[i]
			else:
				i += 1
				break
			i += 1
		scor = float(s[i:])
		scores[name] = scor
	f.close()
		
def update_scoreboard():
	f = open("scoreboard.txt", "w")
	for d in scores:
		f.write(d + ' ' + str(scores[d]) + "\n")
	f.close()

def print_scoreboard():
	for d in scores:
		print(d + ' ' + str(scores[d]))
		
# called when you type "reset" as Player 1's name. 
def reset_scores():
	scores.clear()

def change_turns(p):
	if p == 1:
		return 2
	elif p == 2:
		return 1
		
def save_move(p, c):
	symbol = ''
	if p == 1:
		symbol = 'X'
	else:
		symbol = 'O'
	i = 1
	while True:
		i += 1
		if A[i][c] != '.':
			i -= 1
			break
		if i == 7:
			break
#	print('A[', i, '][', c, '] = ', A[i][c])
	A[i][c] = symbol
#	print('symbol = ', symbol)
	return i

def print_grid():
	for i in range(8):
		print('', end = ' ')
		for j in range(8):
			if i>0 and j>0:
				print(A[i][j], ' ', end = ' ')
		print()
	print('[1] [2] [3] [4] [5] [6] [7]\n')


def is_game_over(r, c, player):
	h = ''; v = ''; d1 = ''; d2 = ''
	if (player == 1):
		strike = 'XXXX'
	else:
		strike = 'OOOO'

	# horizontal check
	for i in range(8):
		h += A[r][i]
	if (strike in h):
		return True

	# vertical check
	for i in range(8):
		v += A[i][c]
	if (strike in v):
		return True

	# 1st diagonal check (top left -> bottom right)
	d1_possible = [(r-6,c-6), (r-5,c-5), (r-4,c-4), (r-3,c-3), (r-2,c-2), (r-1,c-1),
				(r,c), (r+1,c+1), (r+2,c+2), (r+3,c+3), (r+4,c+4), (r+5,c+5), (r+6,c+6)]
	for i in range(len(d1_possible)):
		if(d1_possible[i][0] < 8 and d1_possible[i][0] > 0 and d1_possible[i][1] < 8 and d1_possible[i][1] > 0):
			d1 += A[d1_possible[i][0]][d1_possible[i][1]]
	if (strike in d1):
		return True


	# 2nd diagonal check (bottom left -> top right)
	d2_possible = [(r+6,c-6), (r+5,c-5), (r+4,c-4), (r+3,c-3), (r+2,c-2), (r+1,c-1),
				(r,c), (r-1,c+1), (r-2,c+2), (r-3,c+3), (r-4,c+4), (r-5,c+5), (r-6,c+6)]
	for i in range(len(d2_possible)):
		if(d2_possible[i][0] < 8 and d2_possible[i][0] > 0 and d2_possible[i][1] < 8 and d2_possible[i][1] > 0):
			d2 += A[d2_possible[i][0]][d2_possible[i][1]]
	if (strike in d2):
		return True
	
	return False

def is_tie():
	return (A[1][1] != '.') and (A[1][2] != '.') and (A[1][3] != '.') and (A[1][4] != '.') and (A[1][5] != '.') and (A[1][6] != '.') and (A[1][7] != '.')


def save_draft_move(p, c):
	symbol = ''
	global A
	if p == 1:
		symbol = 'X'
	else:
		symbol = 'O'
	i = 1
	while True:
		i += 1
		if A[i][c] != '.':
			i -= 1
			break
		if i == 7:
			break
#	print('A[', i, '][', c, '] = ', A[i][c])
	A[i][c] = symbol
#	print('symbol = ', symbol)
	return r


def find_cpu_move():
	count = [0,0,0,0,0,0,0,0]
	n = 0
	global A
	A_og = copy.deepcopy(A)
	if dif_level == "EASY":
		n = 100
	elif dif_level == "NORMAL":
		n = 400
	elif dif_level == "HARD":
		n = 600
	elif dif_level == "CRUSHING":
		n = 1000

	for i in range(1,8):
#		print("i=", i)
		print(25*"\n" + "Thinking" + (i%3 + 1)*"." + "\n")
		for j in range(n):
#			print("    j=", j)
			p = 2 # player; 1 for human, 2 for computer
			A = copy.deepcopy(A_og)
			c = i # the i-th column is selected as first CPU move. Then in the while-block we examine if that move was good
			if A[1][c] != '.':
				count[i] = -10000 # this column is already full, so you can't play there
				break
			r = save_draft_move(p,c)
			winner = "NULL"
			moves = 1;
			p = 1 
			while winner == "NULL":
				c = int(7*random.random() + 1)
				while A[1][c] != '.':
					c = int(7*random.random() + 1)
				r = save_draft_move(p,c)

				if is_game_over(r,c,p):
					winner = p
					if winner == 2:
						count[i] += 1
						if moves == 1:
							count[i] += 99
					elif moves == 2:
						count[i] -= 99
#					print("        winner = ", winner)
#					print_grid()
					break
				elif is_tie():
					winner = 0;
					count[i] += 0.5
#					print("   tie")
#					print_grid()
					break
#				print("     c = ", c)
#				print_grid()
				
				p = change_turns(p)
				moves += 1

	maxv = -1; maxi = "NULL"
	for i in range(1, len(count)):
		if count[i] > maxv:
			maxv = count[i]; maxi = i

	print(count)
	A = copy.deepcopy(A_og)
	return maxi

				

playing = True
winner = 0; loser = 0

read_file()
print(scores)
update_scoreboard()

while playing:
	names = [0,0,0]
	print(30*'\n')
	print_scoreboard()
	if scores != {}:
		print("\nTo reset the scoreboard, type reset\n\n")
	else:
		print(3*"\n")
	names[1] = input('Player 1, type your name (no spaces)\n')
	if names[1] == 'reset':
		reset_scores()
		update_scoreboard()
		continue
	names[2] = input('Player 2, type your name (no spaces)\nIf you want to play against the computer, type CPU\n')
	if names[2] == 'reset':
		reset_scores()
		update_scoreboard()
		continue
	if names[2] == "CPU":
		vs_computer = True
		print("Please select the difficulty level:")
		print("1. Easy")
		print("2. Normal")
		print("3. Hard")
		print("4. Crushing")
		a = input()
		if a == "1" or a.upper() == "EASY":
			dif_level = "EASY"
		elif a == "2" or a.upper() == "NORMAL":
			dif_level = "NORMAL"
		elif a == "3" or a.upper() == "HARD":
			dif_level = "HARD"
		elif a == "4" or a.upper() == "CRUSHING":
			dif_level = "CRUSHING"
		names[2] += "_" + dif_level.lower();
	
	player = 1
	
	while True:
		print(30*'\n')

		if player == 1 or (player == 2 and vs_computer == False):
			print_grid()
			if player == 1 and vs_computer == True:
				try:
					c = int(c)
					c = str(c)
				except:
					print()
				else:
					print("The computer has played in the column", c)
			s = names[player] 
			if player == 1:
				s += ' (X) '
			else:
				s += ' (O) '
			s += 'choose a column '
			c = input(s)
			flag = False
			if c.isnumeric():
				c = int(c)
				if c < 8 and c > 0 and A[1][c] == '.':
					flag = True
			while flag == False:
				c = input('Invalid choice, please pick again ')
				if c.isnumeric():
					c = int(c)
					if c < 8 and c > 0 and A[1][c] == '.':
						flag = True
		else: 
			c = find_cpu_move()
		
		r = save_move(player, c)
		if is_game_over(r,c, player):
			winner = player
			loser = change_turns(player)
			break
		if is_tie():
			winner = 0
			break
		player = change_turns(player)
			
	print(30*'\n')
	print_grid()
	
	if (winner == 0):
		print("It's a tie!")
		if names[1] in scores:
			scores[names[1]] += 0.5
		else:
			scores[names[1]] = 0.5
		if names[2] in scores:
			scores[names[2]] += 0.5
		else:
			scores[names[2]] = 0.5
	else: 
		if vs_computer == True and winner == 2:
			print("The computer has played in the column", c)
			print('You lose... ', names[winner], 'is the winnner!')
		else:
			print('Congratulations,', names[winner], '! You won!')
		if names[winner] in scores:
			scores[names[winner]] += 1.0
		else:
			scores[names[winner]] = 1.0
		if names[loser] not in scores:
			scores[names[loser]] = 0.0
	
	update_scoreboard()
	ans = input('If you want to play again, type 1\n')
	if ans != '1':
		playing = False
	else:
		A = [['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.']]
		vs_computer = False
		dif_level = "NONE"
		c = "foo" # just sth that leads to an exception in the try block
	
	
