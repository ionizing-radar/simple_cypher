#!/usr/bin/python
# super simple crypto - substituion cypher by hand
# TODO: ceasar shift
# TODO: Viginere cypher
# TODO: add load function
# TODO: pagination
# TODO: something sexy about printing all the time, write to screen position instead?

import os, sys
import operator

#GLOBALS
DATA_PRINT_LINES = 20 # don't ask, magic numbers are magic
GREEN_TEXT = '\033[1;32;49m'
BLACK_TEXT = '\033[0;37;49m'

last_swap = []

#cuz colours are pretty, and help you see which have been changed
colours={"default":"",
         "blue":   "\x1b[01;34m",
         "cyan":   "\x1b[01;36m",
         "green":  "\x1b[01;32m;49m",
         "red":    "\x1b[01;05;37;41m"}


# frequency of letters in english
english_frequency = {'a':8.167, 'b':1.492, 'c':2.782, 'd':4.253, 'e':12.702, 'f':2.228, 'g':2.015, 			'h':6.094, 'i':6.966, 'j':0.153, 'k':0.772, 'l':4.025, 'm':2.406, 'n':6.749, 'o':7.507, 'p':1.929, 			'q':0.095, 'r':5.987, 's':6.327, 't':9.056, 'u':2.758, 'v':0.978, 'w':2.361, 'x':0.150, 'y':1.974, 			'z':0.074}

#define alphabet dictionary (a = a, b = b...)
alpha = {}
def reset():
	for i in range(26):
		alpha[chr(i+ord('a'))] = [chr(i+ord('a'))] 
	return
reset()

#print the help screen, such as it is
def print_help():
    print
    print 'Commands:' 
    print " reset: reset all swaps made to your alphabet\n"
    print " swap var1 var2: swap two letters, var1 and var2, in your alphabet\n"
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
				if alpha[ch][0] != ch:
					line += GREEN_TEXT + alpha[ch][0] + BLACK_TEXT
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
	for index in range(26):
		key = chr(index+ord('a'))
		aleph = (alpha[key])[0]

		default_colour = BLACK_TEXT

		if in_frequency[key] >= 10 or english_frequency[key] >= 10: gap = ' '
		else: gap = ''

		if alpha[key][0] != key:
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
	
#iterate over input file to count the frequencies
def find_count(input_data):
	char_count = 0
	in_count = [0 for i in range(26)]

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
	for i in range(26):
		#print '{} {:6.3f}'.format(chr(i+ord('a')), float(freq[i] / float(char_count)) * 100)
		key = chr(i+ord('a'))
		value = float(in_count[i] / float(char_count)) * 100 
		in_frequency[key] = value
	return in_frequency


#return key of a value
def key_of(value):
	for key in alpha:
		print 'key {}: value {}'.format(key, alpha[key][0])
		if alpha[key][0] == value: return key
		
#swap position from the alphabet with each other
def swap(from_letter, to_letter):
	# remember this for undoing
	global last_swap
	last_swap = [from_letter, to_letter]

	if alpha[from_letter][0] != from_letter:
		from_letter = key_of(from_letter)
		#print 'from_letter {} has already been changed'.format(from_letter)
	if alpha[to_letter][0] != to_letter:
		to_letter = key_of(to_letter)
		#print 'to_letter {} has already been changed'.format(to_letter)
	
	temp = alpha[from_letter]
	alpha[from_letter] = alpha[to_letter]
	alpha[to_letter] = temp
	return last_swap

#reverse the last swap
def undo():
	swap(last_swap[0], last_swap[1])
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

	# force the terminal window to be 110x32
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=110))

    #open the input file at sys.argv[1]
	in_file = sys.argv[1]
	input_data = open(in_file, 'r').read()
	

	#find frequencies of letters
	in_count = find_count(input_data)
	in_frequency = find_frequency(in_count)

	help = True		#you get a help menu when you start
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
		elif command == 'reset': reset()
		elif command == 'undo': undo()
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
    exit()

