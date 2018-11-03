#!/usr/bin/python
import sys
import re
import string
import textwrap

def reverse_compliment(sequence):
#	compliment = string.translate(sequence, string.maketrans("atcgATCG","tagcTAGC")) #python 2.7.3 compliment sequence complement sequence
	compliment = sequence.translate(str.maketrans("atcgATCG","tagcTAGC")) #python 3.3.2 complement sequence
	reverse = compliment [::-1] #reverse sequence: trick that uses slice notation
	return reverse


if len(sys. argv) <= 0: 
	print("Reverse compliments multiple fasta file")
	exit()

seq_name = ""
seq = ""
seq_names = [] #list of sequence names
seq_name_match = re.compile('^(>.+\s)$') #match fasta header
format_seq = textwrap.TextWrapper(width=70,break_long_words=True)

with open(sys.argv[1], 'r') as file:
	for line in file:
		match = seq_name_match.search(line)
		if match == None:
			seq += line.strip()
		else:
			if seq_name != "":
				print (seq_name)
				formated_seq = format_seq.fill(seq)
				print (formated_seq)
				print ("")
			seq_name = match.group(1).strip()
			seq_names.append(seq_name)
			seq = ""

print (seq_name)
formated_seq = format_seq.fill(seq)
print (formated_seq)
print ("")

file.close()
