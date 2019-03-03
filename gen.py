import pickle
import numpy as np
import sys
from collections import defaultdict

score = dict()
st = set()
r = set()

def turnon():
	
	global r, st, score

	# st contains vocabulary
	# r contains word prefixes
	with open('dicts.pckl', 'rb') as f:
		[st, r] = pickle.load(f)

	# scrabble scores
	for u in 'eaionrtlsu':
		score[u] = 1
	for u in 'dg':
		score[u] = 2
	for u in 'bcmp':
		score[u] = 3
	for u in 'fhvwy':
		score[u] = 4
	for u in 'k':
		score[u] = 5
	for u in 'jx':
		score[u] = 8
	for u in 'qz':
		score[u] = 10

	print ('Loaded scores and vocab.')

# take input
def parser (dim = 4):
	M = []
	for i in range(dim):
		done = False
		while not done:
			inch = False
			l = str(input('line ' + str(i+1) + ': ')).lower()
			R = []
			for u in l:
				if u.isalpha():			# letter
					R.append([u, 1])
				elif u.isdigit():		# multiplier bonus
					R[-1][1] = int(u)
				else: 					# invalid character
					print ('Invalid character: ' + u + '. Try again.')
					inch = True
					break
			if inch:
				continue
			if len(R) > dim:
				print ('More characters than expected. Try again.')
				continue
			elif len(R) < dim:
				print ('Less characters than expected. Try again.')
				continue
			done = True
		M.append(R)
	return M

# word searcher
# ieff, jeff: current position coordinates
# Hcur: occupied positions matrix
# M: word grid
# box: set of words found with score
# curst: string until now
# cscore: score accumulated till now
# mplier: multiplier
def explore (ieff, jeff, Hcur, M, box, curst = '', cscore = 0, mplier = 1):
	i = ieff + 1
	j = jeff + 1

	# add letter to current string. declare location occupied in Hcur
	curst += M[ieff][jeff][0]
	Hcur[i,j] = True

	# update score and bonuses
	if M[ieff][jeff][1] == 4:
		cscore += score[M[ieff][jeff][0]]
		mplier *= 2
	elif M[ieff][jeff][1] == 5:
		cscore += score[M[ieff][jeff][0]]
		mplier *= 3
	else:
		cscore += score[M[ieff][jeff][0]] * M[ieff][jeff][1]

	# if current string is a word, add it to box with score
	if curst in st:
		box[curst] = max(box[curst], cscore*mplier)
	
	cx = [(i+1,j), (i-1,j), (i,j+1), (i,j-1), (i+1,j+1), (i+1,j-1), (i-1,j-1), (i-1,j+1)]	# all directions explorable
	cx = [t for t in cx if not Hcur[t]]														# all locations available
	cs = [curst + M[t[0]-1][t[1]-1][0] for t in cx]											# strings formed with those letters
	cx = [cx[i] for i in range(len(cs)) if cs[i] in r]										# locations that lead to valid words
	for u in cx:
		explore (u[0]-1, u[1]-1, Hcur, M, box, curst, cscore, mplier)						# explore them

	# undoing recursion set up
	# score reset
	if M[ieff][jeff][1] == 4:
		cscore -= score[M[ieff][jeff][0]]
		mplier /= 2
	elif M[ieff][jeff][1] == 5:
		cscore -= score[M[ieff][jeff][0]]
		mplier /= 3
	else:
		cscore -= score[M[ieff][jeff][0]] * M[ieff][jeff][1]

	# location freed and string reset
	Hcur[i,j] = False
	curst = curst[:-1]

# sort by score
def sorter(val):
	return val[1]

# exploration driver
def explorer (M, dim = 4):

	# set up the position occupied matrix
	expdim = dim + 2
	H = np.full((expdim, expdim), False)
	for i in range(expdim):
		H[0,i] = H[-1,i] = H[i,0] = H[i,-1] = True

	# call explore for all starting locations in grid
	box = defaultdict(lambda: 0)
	for i in range(dim):
		for j in range(dim):
			explore(i,j,H,M,box)
	
	# sort words found by score. take only those with length >= 3
	m = list(box.items())
	m.sort(key = sorter, reverse = True)
	m = [u for u in m if len(u[0]) >= 3]
	return m

if __name__ ==  '__main__':
	if len(sys.argv) == 1:		# normal call
		turnon()
		M = parser()
		m = explorer (M)
	elif len(sys.argv) == 2:	# call with dimensions specified
		try:
			dim = int(sys.argv[1])
			if dim < 3:
				raise Exception()
			turnon()
			M = parser(dim)
			m = explorer (M, dim)
			print ('Looking for words...')
		except:
			print ('Incorrect command.')
			print ('Dimension should be an integer >= 3.')
			print ('Usage: python gen.py (optional-dimension)')
			exit()
	else:
		print ('Incorrect command.\nUsage: python gen.py (optional-dimension)')
		exit()

	# write words to cheat.txt
	with open('cheat.txt', 'w') as f:
		try:
			for u in m:
				f.write(u[0] + ' ' + str(u[1]) + '\n')
			print (str(len(m)) + ' words found and written into cheat.txt\nBest of luck!! *wink*')
		except:
			print ('IOError: Could not open cheat.txt for writing.')