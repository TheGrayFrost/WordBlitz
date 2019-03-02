import pickle
import numpy as np
import sys
from collections import defaultdict

score = dict()
st = set()
r = set()

def turnon():
	# dictionary loads
	global r, st
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
				if u.isalpha():
					R.append([u, 1])
				elif u.isdigit():
					R[-1][1] = int(u)
				else:
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
def explore (ieff, jeff, Hcur, M, box, curst = '', cscore = 0, mplier = 1):
	i = ieff + 1
	j = jeff + 1
	curst += M[ieff][jeff][0]
	if M[ieff][jeff][1] == 4:
		cscore += score[M[ieff][jeff][0]]
		mplier *= 2
	elif M[ieff][jeff][1] == 5:
		cscore += score[M[ieff][jeff][0]]
		mplier *= 3
	else:
		cscore += score[M[ieff][jeff][0]] * M[ieff][jeff][1]
	Hcur[i,j] = True
	if curst in st:
		box[curst] = max(box[curst], cscore*mplier)
	if curst in r:
		cx = [(i+1,j), (i-1,j), (i,j+1), (i,j-1), (i+1,j+1), (i+1,j-1), (i-1,j-1), (i-1,j+1)]
		cx = [t for t in cx if not Hcur[t]]
		cs = [curst + M[t[0]-1][t[1]-1][0] for t in cx]
		cx = [cx[i] for i in range(len(cs)) if cs[i] in r]
		for u in cx:
			explore (u[0]-1, u[1]-1, Hcur, M, box, curst, cscore, mplier)
	Hcur[i,j] = False
	curst = curst[:-1]
	if M[ieff][jeff][1] == 4:
		cscore -= score[M[ieff][jeff][0]]
		mplier /= 2
	elif M[ieff][jeff][1] == 5:
		cscore -= score[M[ieff][jeff][0]]
		mplier /= 3
	else:
		cscore -= score[M[ieff][jeff][0]] * M[ieff][jeff][1]

def sorter(val):
	return val[1]

def explorer (M, dim = 4):
	expdim = dim + 2
	box = defaultdict(lambda: 0)
	H = np.full((expdim, expdim), False)
	for i in range(expdim):
		H[0,i] = H[-1,i] = H[i,0] = H[i,-1] = True
	for i in range(dim):
		for j in range(dim):
			explore(i,j,H,M,box)
			#print (box)
	m = list(box.items())
	m.sort(key = sorter, reverse = True)
	return m

if __name__ ==  '__main__':
	# get words
	if len(sys.argv) == 1:
		turnon()
		M = parser()
		m = explorer (M)
	elif len(sys.argv) == 2:
		try:
			dim = int(sys.argv[1])
			if dim < 3:
				raise Exception()
		except:
			print ('Incorrect command.')
			print ('Dimension should be an integer >= 3.')
			print ('Usage: python gen.py (optional-dimension)')
			exit()
		finally:
			turnon()
			M = parser(dim)
			m = explorer (M, dim)
			print ('Looking for words...')
	else:
		print ('Incorrect command.\nUsage: python gen.py (optional-dimension)')
		exit()

	# sort by length and write to cheat.txt
	with open('cheat.txt', 'w') as f:
		try:
			count = 0
			for u in m:
				if (len(u[0]) >= 3):
					f.write(u[0] + ' ' + str(u[1]) + '\n')
					count += 1
			print (str(count) + ' words found and written into cheat.txt\nBest of luck!! *wink*')
		except:
			print ('IOError: Could not open cheat.txt for writing.')