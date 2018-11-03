from Bio import SeqIO
import sys
import os
import glob

path = sys.argv[1]
output_file = sys.argv[2]
output_file_path = os.path.join(path, output_file)

with open(output_file, 'w') as w_file:
    for filename in glob.glob(os.path.join(path, '*.fa')):
        if filename != output_file_path:
            print(filename)
            with open(filename, 'rU') as o_file:
                for seq_record in SeqIO.parse(o_file, 'fasta') :
                    SeqIO.write(seq_record, w_file, 'fasta')
                    w_file.write('\n')


