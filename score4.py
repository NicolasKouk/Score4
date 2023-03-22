A = [['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.'], ['.','.','.','.','.','.','.','.']]

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
#	print(h)
	if (strike in h):
		return True

	# vertical check
	for i in range(8):
		v += A[i][c]
#	print(v)
	if (strike in v):
		return True

	# 1st diagonal check (top left -> bottom right)
	d1_possible = [(r-6,c-6), (r-5,c-5), (r-4,c-4), (r-3,c-3), (r-2,c-2), (r-1,c-1),
				(r,c), (r+1,c+1), (r+2,c+2), (r+3,c+3), (r+4,c+4), (r+5,c+5), (r+6,c+6)]
	for i in range(len(d1_possible)):
		if(d1_possible[i][0] < 8 and d1_possible[i][0] > 0 and d1_possible[i][1] < 8 and d1_possible[i][1] > 0):
			d1 += A[d1_possible[i][0]][d1_possible[i][1]]
#	print(d1)
	if (strike in d1):
		return True


	# 2nd diagonal check (bottom left -> top right)
	d2_possible = [(r+6,c-6), (r+5,c-5), (r+4,c-4), (r+3,c-3), (r+2,c-2), (r+1,c-1),
				(r,c), (r-1,c+1), (r-2,c+2), (r-3,c+3), (r-4,c+4), (r-5,c+5), (r-6,c+6)]
	for i in range(len(d2_possible)):
		if(d2_possible[i][0] < 8 and d2_possible[i][0] > 0 and d2_possible[i][1] < 8 and d2_possible[i][1] > 0):
			d2 += A[d2_possible[i][0]][d2_possible[i][1]]
#	print(d2)
	if (strike in d2):
		return True
	
	return False

player = 1

while True:
	print(20*'\n')
	print_grid()
	s = 'Player ' + str(player) 
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
		break
	player = change_turns(player)
		


print(20*'\n')
print_grid()

print('Congratulations! Player', player, 'is the winner!')