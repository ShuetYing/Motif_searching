#!/usr/bin/python3

import os
import re
import sys
import subprocess

# write the sequence ID and species into a file

with open("interested_seq.fa", "r") as f_input, open("ID_species.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if line.startswith(">"):   # header that contain ID and species
                        wo = line.replace(">", "")
                        list = wo.split()
                        id = list[0]
                        species = re.search(r"\[.*?]", line).group()
                        join = id + ":" + species + '\n'
                        f_output.write(join)


# scan protein sequences to find motif

# use patmatmotifs to generate file in gff format

with open("interested_seq.fa", "r") as f_input:
        for line1, line2 in zip(f_input, f_input):   # first line: header, second line: sequence
                lines = line1 + line2
                file = open("motif_input.fa", "w")   # write the protein sequence in a file and used as input to scan against the prosite db
                file.write(lines)
                file.close()
                cmd = "patmatmotifs motif_input.fa motif.txt -rformat2 gff"
                os.system(cmd)
                cmd2 = "grep -v '#' motif.txt > motif1.txt"
                os.system(cmd2)
                with open("motif_gff.txt", "a") as f_output:   # write all the results into a file
                        read_file = open("motif1.txt", "r")
                        content = read_file.readlines()
                        for line in content:
                                f_output.write(line)   # final output file

print("Motif information for each sequence in gff format is saved in 'motif_gff.txt'")


# use patmatmotifs to generate file in excel format

with open("interested_seq.fa", "r") as f_input:
        for line1, line2 in zip(f_input, f_input):   # first line: header, second line: sequence
                lines = line1 + line2
                file = open("motif_input.fa", "w")   # write the protein sequence in a file and used as input to scan against the prosite db
                file.write(lines)
                file.close()
                cmd = "patmatmotifs motif_input.fa motif.txt -rformat2 excel"
                os.system(cmd)
                with open("motif_excel.txt", "a") as f_output:   # write all the results into a file
                        read_file = open("motif.txt", "r")
                        content = read_file.readlines()
                        for line in content:
                                if not line.startswith("SeqName"):   # remove the header, only write lines that contain motif information
                                        f_output.write(line)   # final output file

print("Motif information for each sequence in excel format is saved in 'motif_excel.txt'")


# use patmatmotifs to generate file in seqtable format

with open("interested_seq.fa", "r") as f_input:
        for line1, line2 in zip(f_input, f_input):   # first line: header, second line: sequence
                lines = line1 + line2
                file = open("motif_input.fa", "w")   # write the protein sequence in a file and used as input to scan against the prosite db
                file.write(lines)
                file.close()
                cmd = "patmatmotifs motif_input.fa motif.txt -rformat2 seqtable"
                os.system(cmd)
                cmd2 = "grep -v '#' motif.txt > motif1.txt"   # remove lines containing #
                os.system(cmd2)
                with open("motif1.txt", "r") as infile, open("motif2.txt", "a") as outfile:
                        content = infile.readlines()
                        for line in content:
                                if 'Start' not in line:   # remove the header
                                        outfile.write(line)

with open("motif2.txt", "r") as f_input, open("motif_seqtable.txt", "a") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.isspace():   # remove empty lines in file
                        f_output.write(line)

print("Motif information for each sequence in seqtable format is saved in 'motif_seqtable.txt'")

motif_seq = []
with open("motif_seqtable.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
                list = line.split()
                seq = list[3]   # motif sequence
                motif_seq.append(seq)   # make motif sequences into a list


# from the ID_species.txt, add the species for each sequence

import pandas as pd

df1 = pd.read_table("motif_gff.txt", header=None)

df1_1 = df1.iloc[:,0]   # first column containing ID

df1_1.to_csv('ID.txt', index=False, header=True)   # write to a file as input for next step

with open("ID_species.txt", "r") as f_input, open("ID.txt", "r") as f_input2, open("species.txt", "w") as f_output:
        lines = f_input.readlines()
        content = f_input2.readlines()[1:]
        for line in lines:   # contain ID and species
                ID = line.split(":")[0]   # sequence ID
                spe = line.split(":")[1]   # species name
                for info in content:   # contain ID
                        if info.startswith(ID):
                                rep = info.replace(info, spe)
                                f_output.write(rep)   # write species name into a file


# read the output files and list from patmatmotifs and convert to data frame

df1 = pd.read_table("motif_gff.txt", header=None)

df2 = pd.read_table("species.txt", header=None)

df3 = pd.read_table("motif_excel.txt", header=None)

df4 = pd.DataFrame(motif_seq, columns = ["Motif sequence"])

info = pd.concat([df1, df2, df3, df4], axis=1)   # join all the 4 data frame horizontally

info.columns = ['ID', 'Function', 'Type', 'Start', 'End', 'Length', 'Empty', 'Empty', 'Comment', 'Species', 'ID', 'Start', 'End', 'Length', 'Strand', 'Motif name', 'Motif sequence']   # rename each column

motif_info = info.iloc[:,[0,9,3,4,5,14,15,16]]   # select columns that contain useful information

motif_info.to_csv('motif_info.csv', index=False, header=True)   # write data frame to file so that user can download

print("Full information of protein motif is saved in 'motif_info.csv'")


# determine whether all the sequence has motif

cmd = "grep '>' interested_seq.fa | wc -l"
no_of_seq = subprocess.check_output(cmd, shell=True).decode("utf-8")
id = motif_info['ID'].unique()   # which ID has motif in the db
no_of_id = len(id)
if int(no_of_seq) == no_of_id:
        print("All sequences have motif!")
else:
        print("There are only " + str(no_of_id) + " sequences with found motif in PROSITE database")


# count the number of occurrence for each motif

no_of_occurrence = motif_info['Motif name'].value_counts(ascending=False)

print("Below is the number of occurrences for each motif:")

print(no_of_occurrence)


# print entire data frame

pd.set_option('display.max_rows', None, 'display.max_columns', None)


# ask user whether they are interested in any particular motif

while True:
        user_input = input("Do you have any particular motif of interest (yes or no)?\n")
        if user_input.lower() == "yes":
                enter = input("Please enter the motif name of interest:\n")
                name = enter.upper()
                print("Information of " + name + " motif")
                call = print(motif_info[motif_info['Motif name'].str.contains(name)])
                ask_again = input("Are they any other motif information you would like to view (yes or no)?\n")
                if ask_again.lower() == "yes":
                        print("OK!")
                elif ask_again.lower() == "no":
                        print("OK! Let's continue!")
                        break
                else:
                        print("Please type yes or no!")
        elif user_input.lower() == "no":
                print("OK!")
                break
        else:
                print("Please type yes or no!")


# remove those files at the end so that user can run the program many times

os.remove("motif_gff.txt")
os.remove("motif_excel.txt")
os.remove("motif_seqtable.txt")
os.remove("motif2.txt")
