#!/usr/bin/python
# super simple crypto - substituion cypher by hand
# TODO: Viginere cypher
# TODO: add load function
# TODO: pagination
# TODO: something sexy about printing all the time, write to screen position instead?

import os, sys
import operator

#GLOBALS
ALPHABET_SIZE = 26
DATA_PRINT_LINES = 20 # don't ask, magic numbers are magic
MIN_COLUMNS = 110
MIN_ROWS = 32
GREEN_TEXT = '\033[1;32;49m'
BLACK_TEXT = '\033[0;37;49m'

#for undo functions
global last_swap
last_swap = []
undo_type = ['swap', 'shift']
SWAP = 0
SHIFT = 1
undo = undo_type[SWAP]

#cuz colours are pretty, and help you see which have been changed
colours={"default":"",
         "blue":   "\x1b[01;34m",
         "cyan":   "\x1b[01;36m",
         "green":  "\x1b[01;32m;49m",
         "red":    "\x1b[01;05;37;41m"}


# frequency of letters in english
english_frequency = {'a':8.167, 'b':1.492, 'c':2.782, 'd':4.253, 'e':12.702, 'f':2.228, 'g':2.015, 			'h':6.094, 'i':6.966, 'j':0.153, 'k':0.772, 'l':4.025, 'm':2.406, 'n':6.749, 'o':7.507, 'p':1.929, 			'q':0.095, 'r':5.987, 's':6.327, 't':9.056, 'u':2.758, 'v':0.978, 'w':2.361, 'x':0.150, 'y':1.974, 			'z':0.074}

#define alphabet dictionary (a = a, b = b...)
alpha = []
def reset():
	global alpha
	alpha = []
	for i in range(ALPHABET_SIZE):
		alpha.append(chr(i+ord('a')))
	return
reset()

#error message, doesn't actually do anything ... yet
def error(message):
	return

#print the help screen, such as it is
def print_help():
	print '\nCommands:' 
	print " reset: reset all swaps made to your alphabet\n"
	print " swap var1 var2: swap two letters, var1 and var2, in your alphabet\n"
	print " shift n: cesear shift by n (neg'tive values work too)"
	print " undo: undo the last swap\n"
	print " save [filename]: save the text, with your custom alphabet, ie: plaintext ... maybe"
	print "     - sets the value of 'filename' as well, but the filename is optional if you already have one\n"
	print " savefile 'name_your_save_file': set the name of your save file\n"
	print " help: this screen\n"
	print " q, quit, or exit: quit without saving, no take backsies\n"
	
	return

#print out the first DATA_PRINT_LINES of the input file
def print_data(input_data):
	print
	lines = 0;
	line = '';
	for ch in input_data:
		if ch == '\n':
			print line
			line = ''
			lines += 1
			if lines > DATA_PRINT_LINES: return
		else:
			if ch != ' ':
				if alpha[ordinal(ch)] != ch:
					line += GREEN_TEXT + alpha[ordinal(ch)] + BLACK_TEXT
				else: line += ch
			else:
				line += ch		
	return

#print the header lines - the freqs and chars of the custom alphabet and of english
def print_screen(in_frequency, character_count):
	line_index = 0;
	char_line  = ' '
	in_f_line  = ''
	en_f_line  = ''
	alpha_line = ' '
	print 'Cypher: {}\nPlaintext: {}'.format(in_file, out_file)
	for index in range(ALPHABET_SIZE):
		key = chr(index+ord('a'))
		aleph = alpha[index]

		default_colour = BLACK_TEXT

		if in_frequency[key] >= 10 or english_frequency[key] >= 10: gap = ' '
		else: gap = ''

		if alpha[index] != key:
			in_f_line += GREEN_TEXT
			alpha_line += GREEN_TEXT

		char_line += gap + '{:4}'.format(key)	
		alpha_line += gap + '{:4}'.format(aleph) + default_colour
	

		if in_frequency[key] >= 1:
			in_f_line += gap +'{:4.1f}'.format(in_frequency[key]) + default_colour
		else:
			next = '{:3.2f}'.format(in_frequency[key])
			in_f_line += gap + " " + next.strip('0') + default_colour


		en_f_line += gap + '{:4.1f}'.format(english_frequency[key]) + default_colour

	print 'Input Data'
	print alpha_line
	print in_f_line
	print 'English'
	print char_line
	print en_f_line
	
	if last_swap != []:
		print 'Undo: {} {}'.format(last_swap[0], last_swap[1])
	else: print ''

	return
	
#give the ordinal value of a letter, with a=0
def ordinal(letter):
	return ord(letter)-ord('a')

#iterate over input file to count the frequencies
def find_count(input_data):
	char_count = 0
	in_count = [0 for i in range(ALPHABET_SIZE)]

	for ch in input_data:
		if ch not in [' ', '\n']:
			char_count += 1
			#print ord(ch), ch, ord(ch)-ord('a')
			in_count[ord(ch)-ord('a')] += 1
	return in_count


#build a dictionary with letters as keys and freqs as values
def find_frequency(in_count):
	char_count = 0
	for i in in_count:
		char_count += int(i)
	in_frequency = {}
	for i in range(ALPHABET_SIZE):
		#print '{} {:6.3f}'.format(chr(i+ord('a')), float(freq[i] / float(char_count)) * 100)
		key = chr(i+ord('a'))
		value = float(in_count[i] / float(char_count)) * 100 
		in_frequency[key] = value
	return in_frequency
		
#swap position from the alphabet with each other
def swap(from_letter, to_letter):
	# remember this for undoing
	global undo
	global last_swap
	undo = undo_type[SWAP]
	last_swap = [from_letter, to_letter]

	from_index = -1
	to_index = -1
	
	for i in range(ALPHABET_SIZE):
		if alpha[i] == from_letter: from_index = i
		if alpha[i] == to_letter: to_index = i
	
	alpha[from_index] = to_letter
	alpha[to_index] = from_letter

	return last_swap

#reverse the last swap
def oops():
	swap(last_swap[0], last_swap[1])
	return

#cesear shift by n
def rotate(n):
	global undo
	undo = undo_type[SHIFT]

	print alpha

	temp = []
	for i in range(ALPHABET_SIZE): 
		shift_index = (i + n) % ALPHABET_SIZE
		temp.append(alpha[shift_index])
	for i in range(ALPHABET_SIZE):
		alpha[i] = temp[i] 

	return

#save the 'corrected' value
def write(outfile, input_data):
	save_data = ''
	for ch in input_data:
		if ch != ' ' and ch != '\n' and alpha[ch][0] != ch:
			save_data += alpha[ch][0]
		else:
			save_data += ch

	out_file = open(outfile, 'w')
	out_file.write(save_data)
	out_file.close()	
	return

def main():
	if len(sys.argv) < 1:
		usage()

	# globals
	global in_file
	global out_file

	# force the terminal window to be at least 110x32
	rows, columns = os.popen('stty size', 'r').read().split()
	rows = int(rows)
	columns = int(columns)
	if columns < MIN_COLUMNS and rows >= MIN_ROWS:
		sys.stdout.write("\x1b[8;{r};{c}t".format(r=rows, c=MIN_COLUMNS))
	elif columns >= MIN_COLUMNS and rows < MIN_ROWS:
		sys.stdout.write("\x1b[8;{r};{c}t".format(r=MIN_ROWS, c=columns))
	elif columns < MIN_COLUMNS and rows < MIN_ROWS:
		sys.stdout.write("\x1b[8;{r};{c}t".format(r=MIN_ROWS, c=MIN_COLUMNS))
	# adjust size of print screen (used for pagination etc)
	global DATA_PRINT_LINES
	DATA_PRINT_LINES += rows - MIN_ROWS

    #open the input file at sys.argv[1]
	in_file = sys.argv[1]
	input_data = open(in_file, 'r').read()
	

	#find frequencies of letters
	in_count = find_count(input_data)
	in_frequency = find_frequency(in_count)

	help = False
	out_file = None
	done = False
	while not done:
		print_screen(in_frequency, in_count)
		if help:
			print_help()
			help = False
		else:
			print_data(input_data)
		command = sys.stdin.readline().rstrip()
		if command == 'help' or command == 'h':
			help = True
		if command == 'exit' or command == 'quit' or command == 'q':
			print 'Bye...'
			done = True
		elif command[:4] == 'swap' and len(command) == 8 and command[5] in alpha and command [7] in alpha:
			last_swap = swap(command[5], command[7])
		elif command == 'reset':
			reset()
		elif command == 'undo':
			print ' undo a thing'
			oops()
			
		elif command[:5] == 'shift':
			shift = 0
			try:
				shift = int(command[-(len(command)-6):].rstrip())
			except:
				error("{} isn't a good shift value".format(command[-(len(command)-6):]))
			if shift != 0: rotate(shift)
		elif (command[:4] == 'save' and len(command) > 5) or (command[:5] == 'save' and len(command) > 6):
			if len(command) > 5:
				out_file = '{}'.format(command[-(len(command)-5):])
			write(out_file, input_data)
		elif command == 'savefile':
			out_file = '{}'.format(command[-(len(command)-9):])		
		else: help = True; #if you got to this point, a help menu might be handy

main()
exit()


def usage():
	print("Usage: %s [in_file] [out_file] [password]" % sys.argv[0])
	print"But that's pretty obsolete, you might have to wAG it"
	exit()

