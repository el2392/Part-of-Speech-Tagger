import re 
import sys
import string
import fileinput
import random

#declare Parts of Speech dictionary, tracks the frequency of each word under a part of speech
POS = {'VB': {}, 'VBP': {}, 'VBZ': {}, 'VBD': {}, 'VBG': {}, 'VBN': {}, 'NNP': {}, 'NNPS': {}, 'NN': {}, 'NNS': {}, 'JJ': {}, 'JJR': {}, 'JJS': {}, 'RB': {}, 'RBR': {}, 'RBS': {}, 'RP': {}, 'PRP': {}, 'PRP$': {}, 'WP': {}, 'WP$': {}, 'WDT': {}, 'WRB': {}, 'CC': {}, 'CD': {}, 'DT': {}, 'PDT': {}, 'IN': {}, 'MD': {}, '#': {}, '$': {}, '.': {}, ',': {}, ':': {}, '``': {}, '\'\'': {}, '(': {}, ')': {}, '\'': {}, 'FW': {}, 'SYM': {}, 'LS': {}, 'TO': {}, 'POS': {}, 'UH': {},'EX': {}}

#declare State dictionary, tracks the frequency of a POS following another POS
STATE = {'Begin_Sent': {}, 'End_Sent': {},'VB': {}, 'VBP': {}, 'VBZ': {}, 'VBD': {}, 'VBG': {}, 'VBN': {}, 'NNP': {}, 'NNPS': {}, 'NN': {}, 'NNS': {}, 'JJ': {}, 'JJR': {}, 'JJS': {}, 'RB': {}, 'RBR': {}, 'RBS': {}, 'RP': {}, 'PRP': {}, 'PRP$': {}, 'WP': {}, 'WP$': {}, 'WDT': {}, 'WRB': {}, 'CC': {}, 'CD': {}, 'DT': {}, 'PDT': {}, 'IN': {}, 'MD': {}, '#': {}, '$': {}, '.': {}, ',': {}, ':': {}, '``': {}, '\'\'': {}, '(': {}, ')': {}, '\'': {}, 'FW': {}, 'SYM': {}, 'LS': {}, 'TO': {}, 'POS': {}, 'UH': {},'EX': {}}

def main():
	#get and open training corpus
	trainingFile = open(sys.argv[1], encoding = "utf8")

	#calls the setup function on the trianing file
	SetupPOS(trainingFile)

	#close training corpus file
	trainingFile.close()	

	#get and open develpment corpus
	devFile = open(sys.argv[2], encoding = "utf8")

	#output file to write to
	finishedFile = open(sys.argv[3], 'w', encoding = 'utf8')

	#calls the assign function on the development and output file
	AssignPOS(devFile, finishedFile)

	#close the development and output files
	devFile.close()
	finishedFile.close()

#parses the corpus, inputs words into POS dictionary with correct statistic frequency 
def SetupPOS(trainingFile):

	#keep track of the previous line for the STATE dictionary
	previousLine = []

	#go through all the lines in the corpus
	for lines in trainingFile:

		#create a list of the line, breaking up the word itself from its POS
		currentLine = lines.split('	')

		if (lines != '\n'):

			#if the word in the POS subdictionary does not exist then create it
			if (POS[currentLine[1].rstrip()].get(currentLine[0]) == None):
				POS[currentLine[1].rstrip()][currentLine[0]] = 1
			#if the word in the POS subdictionary exists then incremenet it
			else:
				POS[currentLine[1].rstrip()][currentLine[0]] = POS[currentLine[1].rstrip()].get(currentLine[0]) + 1

			#if the previous line is a newline or empty then use beginning of sentence
			if (len(previousLine) == 0 or previousLine[0] == '\n'):
				#if the current POS does not exist in the Beginning Sentence subdictionary create it
				if (STATE['Begin_Sent'].get(currentLine[1].rstrip()) == None):
					STATE['Begin_Sent'][currentLine[1].rstrip()] = 1
				#if the current POS does exist in the Beginning Sentence subdictionary then increment it
				else:
					STATE['Begin_Sent'][currentLine[1].rstrip()] = STATE['Begin_Sent'].get(currentLine[1].rstrip()) + 1
			#if the previous line is a POS
			else:
				#if the current POS does not exist in the previous POS subdictionary create it
				if (STATE[previousLine[1].rstrip()].get(currentLine[1].rstrip()) == None):
					STATE[previousLine[1].rstrip()][currentLine[1].rstrip()] = 1
				#if the current POS does exist in the previous POS subdictionary then increment it
				else:
					STATE[previousLine[1].rstrip()][currentLine[1].rstrip()] = STATE[previousLine[1].rstrip()].get(currentLine[1].rstrip()) + 1			
		else:
			#if the previous POS does not exist in the Ending Sentence subdictionary create it
			if (STATE['End_Sent'].get(previousLine[1].rstrip()) == None):
				STATE['End_Sent'][previousLine[1].rstrip()] = 1
			#if the previous POS does exist in the Ending Sentence subdictionary then increment it
			else:
				STATE['End_Sent'][previousLine[1].rstrip()] = STATE['End_Sent'].get(previousLine[1].rstrip()) + 1

		previousLine = currentLine

	#for all keys in the POS subDictionary
	for key, subDictionary in POS.items():
		total = 0

		#get the total frequency in the subdictionary
		for skey, value in subDictionary.items():
			total += value

		#calculate and set the probably of each word in the subdictionary
		for skey in subDictionary:
			subDictionary[skey] = subDictionary[skey]/total


	#for all keys in the STATE subDictionary
	for key, subDictionary in STATE.items():
		total = 0

		#get the total frequency in the subdictionary
		for skey, value in subDictionary.items():
			total += value

		#calculate and set the probably of each word in the subdictionary
		for skey in subDictionary:
			subDictionary[skey] = subDictionary[skey]/total

#finds POS of a word based on statistic frequency
def AssignPOS(devFile, finishedFile):

	#tokenized version of the sentence to iterate through
	tokenized = []

	#iterating through all the lines in the development file
	for lines in devFile:

		#if the line has text and is not a new line
		if (lines != '\n'):
			#strip the new line and append to tokenized list
			line = lines.rstrip()
			tokenized.append(line)
		#if the text is a new line, then it is the end of a sentence
		else:
			#create a two dimensional array with the length of the sentence plus 2 for Begin_Sent and End_Sent and with a height of every possible state
			transducer = [[0 for x in range(len(tokenized) + 2)] for y in range(len(STATE))]

			#a way to transverse the column through associated state names and numbers, sort of like enum
			column = {
				'Begin_Sent': 0,
				'VB': 1,
				'VBP': 2,
				'VBZ': 3,
				'VBD': 4,
				'VBG': 5,
				'VBN': 6,
				'NNP': 7,
				'NNPS': 8,
				'NN': 9,
				'NNS': 10,
				'JJ': 11,
				'JJR': 12,
				'JJS': 13,
				'RB': 14,
				'RBR': 15,
				'RBS': 16,
				'RP': 17,
				'PRP': 18,
				'PRP$': 19,
				'WP': 20,
				'WP$': 21,
				'WDT': 22,
				'WRB': 23,
				'CC': 24,
				'CD': 25,
				'DT': 26,
				'PDT': 27,
				'IN': 28,
				'MD': 29,
				'#': 30,
				'$': 31,
				'.': 32,
				',': 33,
				':': 34,
				'``': 35,
				'\'\'': 36,
				'(': 37,
				')': 38,
				'\'': 39,
				'FW': 40,
				'SYM': 41,
				'LS': 42,
				'TO': 43,
				'POS': 44,
				'UH': 45,
				'EX': 46,
				'End_Sent': 47,
				0: 'Begin_Sent',
				1: 'VB',
				2: 'VBP',
				3: 'VBZ',
				4: 'VBD',
				5: 'VBG',
				6: 'VBN',
				7: 'NNP',
				8: 'NNPS',
				9: 'NN',
				10: 'NNS',
				11: 'JJ',
				12: 'JJR',
				13: 'JJS',
				14: 'RB',
				15: 'RBR',
				16: 'RBS',
				17: 'RP',
				18: 'PRP',
				19: 'PRP$',
				20: 'WP',
				21: 'WP$',
				22: 'WDT',
				23: 'WRB',
				24: 'CC',
				25: 'CD',
				26: 'DT',
				27: 'PDT',
				28: 'IN',
				29: 'MD',
				30: '#',
				31: '$',
				32: '.',
				33: ',',
				34: ':',
				35: '``',
				36: '\'\'',
				37: '(',
				38: ')',
				39: '\'',
				40: 'FW',
				41: 'SYM',
				42: 'LS',
				43: 'TO',
				44: 'POS',
				45: 'UH',
				46: 'EX',
				47: 'End_Sent'
			}

			#the beginning of the sentence always has 100% rate
			transducer[column['Begin_Sent']][0] = 1

			#input the probabilities of the each element of the transducer
			for y in range(len(transducer[0])):
				for x in range(len(transducer)):
					if(y < len(tokenized) and x != 0):

						#check to see if the word is in the POS dictionary, aka if it is known
						known = 0
						for key, subDictionary in POS.items():
							if (subDictionary.get(tokenized[y]) != None):
								known = 1

						#if the word has been seen before
						if (known != 0):
							if (y == 0 and x != 47):
								if (STATE['Begin_Sent'].get(column[x]) != None and POS[column[x]].get(tokenized[y]) != None):
									transducer[x][y+1] = STATE['Begin_Sent'].get(column[x]) * POS[column[x]].get(tokenized[y])
								elif (STATE['Begin_Sent'].get(column[x]) == None and POS[column[x]].get(tokenized[y]) != None):
									transducer[x][y+1] = POS[column[x]].get(tokenized[y])
								elif (STATE['Begin_Sent'].get(column[x]) != None and POS[column[x]].get(tokenized[y]) == None):
									transducer[x][y+1] = STATE['Begin_Sent'].get(column[x])
								else:
									transducer[x][y+1] = 0
							elif (y == len(tokenized)):
								previousHighest = 0
								previousState = 0
								for z in range(len(transducer)):
									if (previousHighest < transducer[z][y]):
										previousHighest = transducer[z][y]
										previousState = z
								if (STATE[column[previousState]].get('End_Sent') != None):
									transducer[x][y+1] = STATE[column[previousState]].get('End_Sent') * previousHighest
								elif (STATE[column[previousState]].get('End_Sent') == None):
									transducer[x][y+1] = previousHighest
								else:
									transducer[x][y+1] = 0
							else:
								if (x != 47):
									previousHighest = 0
									previousState = 0
									for z in range(len(transducer)):
										if (previousHighest < transducer[z][y]):
											previousHighest = transducer[z][y]
											previousState = z
									if (STATE[column[previousState]].get(column[x]) != None and POS[column[x]].get(tokenized[y]) != None):
										transducer[x][y+1] = STATE[column[previousState]].get(column[x]) * previousHighest * POS[column[x]].get(tokenized[y])
									elif (STATE[column[previousState]].get(column[x]) == None and POS[column[x]].get(tokenized[y]) != None):
										transducer[x][y+1] = previousHighest * POS[column[x]].get(tokenized[y])
									elif (STATE[column[previousState]].get(column[x]) != None and POS[column[x]].get(tokenized[y]) == None):
										transducer[x][y+1] = STATE[column[previousState]].get(column[x]) * previousHighest
									else:
										transducer[x][y+1] = 0
						#if the word has not been encountered then it is an unknown word and given a random probability
						else:
							unknown = tokenized[y]

							if (unknown[-2:] == 'ed'):
								num = random.randint(0, 2)
								if (num == 0):
									transducer[column['JJ']][y+1] = 1
								elif (num == 1):
									transducer[column['VBD']][y+1] = 1
								else:
									transducer[column['VBN']][y+1] = 1
							elif (unknown[-1:] == 's'):
								num = random.randint(0, 1)
								if (num == 0):
									transducer[column['VBZ']][y+1] = 1
								else:
									transducer[column['NNS']][y+1] = 1
							elif (unknown[-3:] == 'ing'):
								num = random.randint(0, 1)
								if (num == 0):
									transducer[column['VBG']][y+1] = 1
								else:
									transducer[column['JJ']][y+1] = 1
							elif (unknown[-2:] == 'er'):
								num = random.randint(0, 1)
								if (num == 0):
									transducer[column['NN']][y+1] = 1
								else:
									transducer[column['JJR']][y+1] = 1
							elif (unknown[-2:] ==  'en'):
								num = random.randint(0, 1)
								if (num == 0):
									transducer[column['NNS']][y+1] = 1
								else:
									transducer[column['VBN']][y+1] = 1
							elif (unknown[-3:] == 'est'):
								transducer[column['JJS']][y+1] = 1
							elif (unknown[-2:] == 'ly'):
								transducer[column['RB']][y+1] = 1
							elif (unknown.isupper()):
								transducer[column['UH']][y+1] = 1
							elif (re.match('([0-9])+', unknown)):
								transducer[column['LS']][y+1] = 1
							elif (unknown[0].isupper()):
								transducer[column['NNP']][y+1] = 1
							elif (re.match('[A-z]+-[A-z]+', unknown)):
								transducer[column['NN']][y+1] = 1
							else:
								num = random.randint(0, 3)
								if (num == 0):
									transducer[column['JJ']][y+1] = 1
								elif (num == 1):
									transducer[column['VB']][y+1] = 1
								elif (num == 2):
									transducer[column['NN']][y+1] = 1
								else:
									transducer[column['RB']][y+1] = 1

			#iterate though all the columns of the transducer
			for y in range(len(transducer[0])):
				#keep tracks of which entry in the column is highest
				highest = 0
				hx = 0
				hy = 0
				#iterate though all the rows of the transducer
				for x in range(len(transducer)):
					#if the current transducer probability is higher than the current highest
					if (transducer[x][y] > highest):
						#update the highest so far and its parameters
						highest = transducer[x][y]
						hx = x
						hy = y
				#throughout the whole transducer, write to the file the entry in each column with the highest score and its corresponding POS
				if (hx!= 0 and hy != 0): #and hx != len(tokenized)+1 and hy != len(STATE)+1
					finishedFile.write(tokenized[hy-1] + '\t' + column[hx] + '\n')

			#clear the list containing the sentence
			tokenized.clear()

			#new line for output
			finishedFile.write('\n')

if __name__ == "__main__":
      main()