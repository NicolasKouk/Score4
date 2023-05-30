A = [['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.']]

scores = {}

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

def save_draft_move(table, p, c):
	symbol = ''
	if p == 1:
		symbol = 'X'
	else:
		symbol = 'O'
	i = 1
	while True:
		i += 1
		if table[i][c] != '.':
			i -= 1
			break
		if i == 7:
			break
#	print('A[', i, '][', c, '] = ', table[i][c])
	table[i][c] = symbol
#	print('symbol = ', symbol)
	return (table, i)


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


def find_cpu_move(dif_level):
	count = [0,0,0,0,0,0,0]
	if dif_level == "EASY":
		n = 20
	elif dif_level == "NORMAL":
		n = 50
	elif dif_level == "HARD":
		n = 100
	elif dif_level == "CRUSHING":
		n = 300

	for i in range(7):
		for j in range(n):
			c = i;
			winner = "NULL"
			while winner == "NULL":
				print()
				if is_game_over(r,c,player):
					winner = player;
					count[i] += 1
				elif is_tie():
					winner = 0;
					count[i] += 0.5

playing = True
winner = 0; loser = 0

read_file()
print(scores)
update_scoreboard()

while playing:
	names = [0,0,0]
	print(30*'\n')
	print_scoreboard()
	print(3*"\n")
	names[1] = input('Player 1, type your name (no spaces)\n')
	if names[1] == 'reset':
		reset_scores()
		update_scoreboard()
		continue
	names[2] = input('Player 2, type your name (no spaces)\n')
	
	player = 1
	
	while True:
		print(20*'\n')
		print_grid()
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
		
		r = save_move(player, c)
		if is_game_over(r,c, player):
			winner = player
			loser = change_turns(player)
			break
		if is_tie():
			winner = 0
			break
		player = change_turns(player)
			
	print(20*'\n')
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
		print('Congratulations,', names[winner], '! You won!')
		if names[winner] in scores:
			scores[names[winner]] += 1
		else:
			scores[names[winner]] = 1
		if names[loser] not in scores:
			scores[names[loser]] = 0
	
	update_scoreboard()
	ans = input('If you want to play again, type 1\n')
	if ans != '1':
		playing = False
	else:
		A = [['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.']]
	
	
