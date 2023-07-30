#!/usr/bin/python3

import os

# identify helix-turn-helix motif which is a nucleic acid binding motifs in protein sequences

# generate result in gff format

cmd = "helixturnhelix interested_seq.fa binding_motif.txt -rformat2 gff"
os.system(cmd)
with open("binding_motif.txt", "r") as f_input, open("binding_motif_gff.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.startswith("#"):   # remove line with #
                        f_output.write(line)


# generate result in excel format

cmd = "helixturnhelix interested_seq.fa binding_motif.txt -rformat2 excel"
os.system(cmd)
with open("binding_motif.txt", "r") as f_input, open("binding_motif_excel.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.startswith("SeqName"):   # remove the header, only write lines that contain motif information
                        f_output.write(line)


# generate file in seqtable format

cmd = "helixturnhelix interested_seq.fa binding_motif.txt -rformat2 seqtable"
os.system(cmd)
with open("binding_motif.txt", "r") as f_input, open("binding_motif1.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.startswith("#"):   # remove line with #
                        f_output.write(line)

with open("binding_motif1.txt", "r") as f_input, open("binding_motif2.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if "Start" not in line:   # remove the header
                        f_output.write(line)

with open("binding_motif2.txt", "r") as f_input, open("binding_motif_seqtable.txt", "w") as f_output:
        content = f_input.readlines()
        for line in content:
                if not line.isspace():   # remove empty lines in file
                        f_output.write(line)

binding_motif = []
with open("binding_motif_seqtable.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
                list = line.split()
                seq = list[4]   # binding motif sequence
                binding_motif.append(seq)   # make motif sequences into a list


# from the ID_species.txt, add the species for each sequence

import pandas as pd

df1 = pd.read_table("binding_motif_gff.txt", header=None)

df1_1 = df1.iloc[:,0]   # first column containing ID

df1_1.to_csv('bm_ID.txt', index=False, header=True)   # write to a file as input for next step

with open("ID_species.txt", "r") as f_input, open("bm_ID.txt", "r") as f_input2, open("species.txt", "w") as f_output:
        lines = f_input.readlines()
        content = f_input2.readlines()[1:]
        for line in lines:   # contain ID and species
                ID = line.split(":")[0]   # sequence ID
                spe = line.split(":")[1]   # species name
                for info in content:   # contain ID
                        if info.startswith(ID):
                                rep = info.replace(info, spe)
                                f_output.write(rep)   # write species name into a file


# read the output files and list and convert to data frame

df1 = pd.read_table("binding_motif_gff.txt", header=None)

df2 = pd.read_table("species.txt", header=None)

df3 = pd.read_table("binding_motif_excel.txt", header=None)

df4 = pd.DataFrame(binding_motif, columns = ["Motif sequence"])

info = pd.concat([df1, df2, df3, df4], axis=1)   # join all the 4 data frame horizontally

info.columns = ['ID', 'Function', 'Type', 'Start', 'End', 'Score', 'Empty', 'Empty', 'Comment', 'Species', 'ID', 'Start', 'End', 'Score', 'Strand', 'Max. score position', 'SD', 'Sequence']

binding_motif_info = info.iloc[:,[0,9,3,4,5,14,15,17]]   # select columns that contain useful information


# find whether there is any nucleic acid binding motif in the protein sequences

no_of_binding_motif = len(binding_motif_info)
if no_of_binding_motif == 0:
        print("There is no nucleic acid binding motif found in the protein sequences...")
else:
        print("Number of nucleic acid binding motif in the protein sequences:" , no_of_binding_motif)
        binding_motif_info.to_csv('binding_motif_info.csv', index=False, header=True)   # write data frame to file so that user can download
        print("Protein sequence containing helix-turn-helix motif that suggest the protein function including DNA binding,\nespecially transcription factor that regulate gene expression:")
        print(binding_motif_info[['ID','Species']])
        print("More information of the protein sequences that contain HTH motif is saved in 'binding_motif_info.csv'")
