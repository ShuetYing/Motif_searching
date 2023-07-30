#!/usr/bin/python3

import os

# use antigenic function in emboss to predict the potential antigenic regions in protein sequences which might be useful for the study or development of synthetic
 peptide vaccine or probe of antibody

# generate file in gff format

cmd = "antigenic interested_seq.fa antigenic.txt -minlen 6 -rformat2 gff"
os.system(cmd)
with open("antigenic.txt", "r") as f_input, open("antigenic_gff.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.startswith("#"):
                        f_output.write(line)


# generate file in excel format

cmd = "antigenic interested_seq.fa antigenic.txt -minlen 6 -rformat2 excel"
os.system(cmd)
with open("antigenic.txt", "r") as f_input, open("antigenic_excel.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.startswith("SeqName"):
                        f_output.write(line)


# generate file in seqtable format

cmd = "antigenic interested_seq.fa antigenic.txt -minlen 6 -rformat2 seqtable"
os.system(cmd)
with open("antigenic.txt", "r") as f_input, open("antigenic1.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.startswith("#"):
                        f_output.write(line)

with open("antigenic1.txt", "r") as f_input, open("antigenic2.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if "Start" not in line:
                        f_output.write(line)

with open("antigenic2.txt", "r") as f_input, open("antigenic_seqtable.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.isspace():
                        f_output.write(line)

antigenic_region = []
with open("antigenic_seqtable.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
                list = line.split()
                region = list[3]
                antigenic_region.append(region)


# convert the output files to data frame

import pandas as pd

df1 = pd.read_table("antigenic_gff.txt", header=None)

df2 = pd.read_table("antigenic_excel.txt", header=None)

df3 = pd.DataFrame(antigenic_region, columns = ["Sequence"])

Ag = pd.concat([df1, df2, df3], axis=1)

Ag.columns = ['ID', 'Function', 'Type', 'Start', 'End', 'Score', 'Empty', 'Empty', 'Comment', 'ID', 'Start', 'End', 'Score', 'Strand', 'Max score position', 'Sequence']

Ag_info = Ag.iloc[:,[0,3,4,5,13,14,15]]

Ag_info.to_csv('Ag_info.csv', index=False, header=True)

print("Information of potential antigenic region of the protein sequences is saved in 'Ag_info.csv'")


# remove those files so that user can use the program many times

os.remove("antigenic_gff.txt")
os.remove("antigenic_excel.txt")
os.remove("antigenic_seqtable.txt")
os.remove("antigenic1.txt")
os.remove("antigenic2.txt")
