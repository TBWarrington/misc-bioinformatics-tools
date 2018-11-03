#!/usr/bin/python
import sys
import re
import string

def reverse_compliment(sequence):
	compliment = string.translate(sequence, string.maketrans("atcgATCGkmryswbvhdKMRYSWBVDH","tagcTAGCmkyrswvbdhMKYRSWVBDH")) #python 2.7.5 compliment sequence complement sequence (includes ambiguity codes)
#	compliment = sequence.translate(str.maketrans("atcgATCGkmryswbvhdKMRYSWBVDH","tagcTAGCmkyrswvbdhMKYRSWVBDH")) #python 3.3.2 complement sequence (includes ambiguity codes)
	reverse = compliment [::-1] #reverse sequence: trick that uses slice notation
	return reverse

def remove_ambiguity(pattern):
	ambiguity_codes = {"k":"[gt]", "m":"[ac]", "r":"[ag]", "y":"[ct]", "s":"[cg]", "w":"[at]", "b":"[cgt]", "v":"[acg]", "h":"[act]", "d":"[agt]", "n":"[gatcn]","K":"[GT]", "M":"[AC]", "R":"[AG]", "Y":"[CT]", "S":"[CG]", "W":"[AT]", "B":"[CGT]", "V":"[ACG]", "H":"[ACT]", "D":"[AGT]", "N":"[GATCN]"}
	for i, j in ambiguity_codes.iteritems(): #python 2.7.5
#	for i, j in ambiguity_codes.items(): #python 3.3.2
		pattern = pattern.replace(i, j)
	return pattern

if len(sys. argv) <= 1: 
	print("Searches fasta file for any number of motifs")
	exit()

seq_name = ""
seq = ""
seq_names = [] #list of sequence names
seq_name_match = re.compile('^>(.+)\s$') #match fasta header
patterns = [] # list of patterns
rev_patterns = [] #reverse compliment of patterns
number = 0 #id count
motif = [] #list of input motifs
print ("##gff-version 3")

for x in sys.argv[2:]: #takes command line arguments and adds to list of patterns (starting st argument 2, 0 is scriptname, 1 file name
	motif.append(x)
	y = '(?=(%s))' % (remove_ambiguity(x)) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns.append(pattern)
	z = '(?=(%s))' % remove_ambiguity((reverse_compliment(x))) # needed to find overlapping matches
	rev_pattern = re.compile(z, re.IGNORECASE)
	rev_patterns.append(rev_pattern)

with open(sys.argv[1], 'r') as file:
	for line in file:
		match = seq_name_match.search(line)
		if match == None:
			seq += line.strip()
		else:
			if seq_name != "":
				#print (seq_name)
				#print (seq)
				motif_num = -1
				for index, stuff in enumerate (patterns):
					matches = stuff.finditer(seq)
					for thing in matches:
						number += 1
						name = str(seq_name)
						start = str(thing.start(1) + 1)
						end = str(thing.end(1))
						sequence = str(thing.group(1))
						input_motif = motif[index]
						print ("".join([name, "\t", input_motif, "\tregex\t", start, "\t", end, "\t.\t+\t.\tID=", name, "_", str(number), ";Sequence=", sequence]))
						#print (thing.group(1))
						#print (thing.start(1) + 1 , thing.end(1))
				for index, stuff in enumerate(rev_patterns):
					matches = stuff.finditer(seq)
					for thing in matches:
						number += 1
						name = str(seq_name)
						start = str(thing.start(1) + 1)
						end = str(thing.end(1))
						sequence = str(thing.group(1))
						input_motif = motif[index]
						print ("".join([name, "\t", input_motif, "\tregex\t", end, "\t", start, "\t.\t-\t.\tID=", name, "_", str(number), ";Sequence=", sequence]))
						#print (thing.group(1))
						#print (thing.start(1) + 1 , thing.end(1))
			number = 0
			seq_name = match.group(1).strip()
			seq_names.append(seq_name)
			seq = ""

#print (seq_name)
#print (seq)
#following needed to capture last sequence, loop ends before output happens
for index, stuff in enumerate (patterns):
	matches = stuff.finditer(seq)
	for thing in matches:
		number += 1
		name = str(seq_name)
		start = str(thing.start(1) + 1)
		end = str(thing.end(1))
		sequence = str(thing.group(1))
		input_motif = motif[index]
		print ("".join([name, "\t", input_motif, "\tregex\t", start, "\t", end, "\t.\t+\t.\tID=", name, "_", str(number), ";Sequence=", sequence]))
		#print (thing.group(1))
		#print (thing.start(1) + 1 , thing.end(1))
for index, stuff in enumerate(rev_patterns):
	matches = stuff.finditer(seq)
	for thing in matches:
		number += 1
		name = str(seq_name)
		start = str(thing.start(1) + 1)
		end = str(thing.end(1))
		sequence = str(thing.group(1))
		input_motif = motif[index]
		print ("".join([name, "\t", input_motif, "\tregex\t", end, "\t", start, "\t.\t-\t.\tID=", name, "_", str(number), ";Sequence=", sequence]))
		#print (thing.group(1))
		#print (thing.start(1) + 1 , thing.end(1))
file.close()
