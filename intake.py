import pickle
import sys

class IFExep (Exception):
	def __init__ (self, w):
		self.w = w

def intake(file):
	# read file and verify format
	try:
		with open(file) as word_file:
			print ('Reading file...')
			st = word_file.read().split()
			print ('File read and format verified.')
		for w in st:
			if not w.isalpha():
				raise IFExep(w)
	except IFExep as ife:
		print ('InputFormatError: Got word \'' + ife.w + '\'. File not in proper format.')
		return
	except:
		print ('FileError: File ' + file + ' not found.')
		return

	# take input from file
	print ('Memorizing words...')
	st = [x.lower() for x in st]
	st = set(st)
	r = set()
	for u in st:
		for i in range(len(u)+1):
			r.add(u[:i])
	print ('Vocabulary building completed.')

	#write out to correct location
	try:
		with open('dicts.pckl', 'wb') as f:
			pickle.dump([st, r], f)
	except:
		print ('IOError: Could not open dicts.pckl for writing.')

	print ('Memory dump completed.\nLearnt ' + str(len(st)) + ' words.')

if __name__ ==  '__main__':
	if len(sys.argv) != 2:
		print ('Incorrect command.\nUsage: python intake.py /path/to/your/word/list')
	else:
		intake(sys.argv[1])