#!/usr/bin/python
import sys
import re
import string

seq_name = ""
seq = ""
seq_names = [] #list of sequence names
seq_name_match = re.compile('^>(.+)\s$') #match fasta header
patterns_single = [] # list of patterns
patterns_half = []
patterns_half_rev = []

patterns_depleted = []
patterns_neutral = []
patterns_enriched = []


stats_single = ["a", "c", "t", "g"]

stats_half = ["aa", "at", "ac", "ag", "ca", "ct", "cc", "cg"]
stats_half_rev = ["tt", "ta", "tg", "tc", "gt", "ga", "gg", "gc"]

nucleosome_depleted = ["aaa", "aat", "ata", "att", "gaa", "taa", "tat", "tta", "ttt"] #trinucleotides that are depleted in nucleosomes
nucleosome_neutral = ["aac", "aag", "aca", "act", "aga", "agg", "agt", "atg", "caa", "cat", "cga", "cta", "ctt", "gcg", "gat", "gca", "gcg", "gga", "ggg", "ggt", "gta", "gtt", "tac", "tag", "tca", "tga", "tgt", "ttc", "ttg"] #trinucleotides that are neither enriched nor depleted in nucleosomes
nucleosome_enriched = ["acc", "acg", "agc", "atc", "cac", "cag", "cca", "ccc", "ccg", "cct", "cgc", "cgg", "cgt", "ctc", "ctg", "gac", "gcg", "ggc", "gct", "gtc", "gtg", "tcc", "tcg", "tct", "tgc", "tgg"] #trinucleotides that are enriched in nucleosomes

n = re.compile('(?=(n))', re.IGNORECASE)
nfreq = {}

for x in stats_single:
	y = '(?=(%s))' % (x) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns_single.append(pattern)
for x in stats_half:
	y = '(?=(%s))' % (x) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns_half.append(pattern)
for x in stats_half_rev:
	y = '(?=(%s))' % (x) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns_half_rev.append(pattern)

for x in nucleosome_depleted: 
	y = '(?=(%s))' % (x) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns_depleted.append(pattern)
for x in nucleosome_neutral: 
	y = '(?=(%s))' % (x) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns_neutral.append(pattern)
for x in nucleosome_enriched: 
	y = '(?=(%s))' % (x) # needed to find overlapping matches
	pattern = re.compile(y, re.IGNORECASE) 
	patterns_enriched.append(pattern)

with open(sys.argv[1], 'r') as file:
	for line in file:
		match = seq_name_match.search(line)
		if match == None:
			seq += line.strip()
		else:
			if seq_name != "":
				print (seq_name)
				nn = n.findall(seq)
				length = len(seq) - len(nn) #length without "N"s

				for index, stuff in enumerate(patterns_single):
					matches = stuff.findall(seq)
					nfreq[stats_single[index]] = (len(matches)/length)
					print (stats_single[index], "=", len(matches)/length)
				for index, stuff in enumerate(patterns_half):
					matches = stuff.findall(seq)
					rev_matches = patterns_half_rev[index].findall(seq)
					print (stats_half[index], "+", stats_half_rev[index], "=", len(matches)/length)
				depleted = 0
				for stuff in patterns_depleted:
					matches = stuff.findall(seq)
					depleted += len(matches)
				print ("Depleted in nucleosomes = ", depleted/length)
				neutral = 0
				for stuff in patterns_neutral:
					matches = stuff.findall(seq)
					neutral += len(matches)
				print ("Neutral in nucleosomes = ", neutral/length)
				enriched = 0
				for stuff in patterns_enriched:
					matches = stuff.findall(seq)
					enriched += len(matches)
				print ("Enriched in nucleosomes = ", enriched/length)
					
			seq_name = match.group(1).strip()
			seq_names.append(seq_name)
			seq = ""
			nfreq = {}

print (seq_name)
nn = n.findall(seq)
length = len(seq) - len(nn) #length without "N"s

for index, stuff in enumerate(patterns_single):
	matches = stuff.findall(seq)
	nfreq[stats_single[index]] = (len(matches)/length)
	print (stats_single[index], "=", len(matches)/length)
for index, stuff in enumerate(patterns_half):
	matches = stuff.findall(seq)
	rev_matches = patterns_half_rev[index].findall(seq)
	print (stats_half[index], "+", stats_half_rev[index], "=", len(matches)/length)
depleted = 0
for stuff in patterns_depleted:
	matches = stuff.findall(seq)
	depleted += len(matches)
print ("Depleted in nucleosomes = ", depleted/length)
neutral = 0
for stuff in patterns_neutral:
	matches = stuff.findall(seq)
	neutral += len(matches)
print ("Neutral in nucleosomes = ", neutral/length)
enriched = 0
for stuff in patterns_enriched:
	matches = stuff.findall(seq)
	enriched += len(matches)
print ("Enriched in nucleosomes = ", enriched/length)

file.close()
