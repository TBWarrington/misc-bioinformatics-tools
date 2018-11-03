from Bio import SeqIO
import sys
import textwrap

gbk_filename = sys.argv[1]
faa_filename = sys.argv[2]
input_handle  = open(gbk_filename, "r")
output_handle = open(faa_filename, "w")

format_seq = textwrap.TextWrapper(width=70,break_long_words=True)

for seq_record in SeqIO.parse(input_handle, "genbank") :
    print("Dealing with GenBank record %s" % seq_record.id)
    seq = str(seq_record.seq)
    formated_seq = format_seq.fill(seq)
    output_handle.write(">%s %s\n%s\n\n" % (
           seq_record.id,
           seq_record.description,
           formated_seq))

output_handle.close()
input_handle.close()

