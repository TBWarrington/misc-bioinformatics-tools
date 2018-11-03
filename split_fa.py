import sys
from Bio import SeqIO

fa_file = sys.argv[1]
counter = 1
file_no_ext = fa_file.split(".")[0]

print(file_no_ext)

file = open(sys.argv[1]).readlines()
str = ''.join(file)

temp = str.split('>')
for i in temp:
	if i:
		filename = "%s_%s.fa" % (file_no_ext, counter)
		output_handle = open(filename, "w")
		output_handle.write ('>' + i)
		counter += 1

