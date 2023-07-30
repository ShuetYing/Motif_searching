#!/usr/bin/python3

import os, subprocess, sys, re


# check the output of esearch


# rerun the user input script

def rerun_input():
        exec(open('user_input.py').read())


# rerun analysis of protein sequences which is this script

def rerun_analysis():
        exec(open('prot_seq.py').read())


# define a function to ask user whether to continue with the current sequence result

def yes_or_no():
        ask_user = input("Do you want to continue with the current dataset (yes or no)?\n")
        if ask_user.lower() == 'yes':
                print("Of course, we will continue with the current sequence set!")
                print('Total number of protein sequences from the search result:', no_of_seq)
        elif ask_user.lower() == 'no':
                print("Please re-enter the protein family and taxon ID")
                rerun_input()   # ask user to input protein and ID
                rerun_analysis()   # analyze the number of protein sequences
        else:
                print("Please type yes or no!")
                yes_or_no()


# define a few conditions in a if loop

while True:
        cmd = "grep '>' raw_sequences.fa | wc -l"
        no_of_seq = subprocess.check_output(cmd, shell=True).decode("utf-8")   # count the number of sequences get from the database
        if 50 < int(no_of_seq) < 1000:   # if the number of sequences is between 50 and 1000, then exit loop
                print("Total number of protein sequences from the search result:", no_of_seq)
                break
        elif int(no_of_seq) > 1000:   # if there are more than 1000 sequences, then ask user some questions
                print("Oops, there are too many sequences!")
                yes_or_no()
                break
        elif int(no_of_seq) < 50:   # if there are less than 50 sequences, then ask user some questions
                print("Oops, there are not much sequences! You might not get useful information.")
                yes_or_no()
                break
        elif int(no_of_seq) == 0:   # if get nothing from the database, ask user to re-enter the query
                print("Sorry, there is no result from the search input. Please try again! (p.s. typo error?)")
                rerun_input()
                rerun_analysis()
                break
        else:
                print("Processing the protein sequences!")


# convert multiline fasta file into single line fasta file where the sequence is in one line

def convert(input, output):
        with open(input) as f_input, open(output, "w") as f_output:
                seq = []
                for line in f_input:
                        if line.startswith(">"):
                                if seq:
                                        f_output.write(''.join(seq) + '\n')
                                        seq = []
                                f_output.write(line)
                        else:
                                seq.append(line.strip())
                if seq:
                        f_output.write(''.join(seq) + '\n')


convert("raw_sequences.fa", "two_lines_seq.fa")   # two lines for each entry: header and sequence


# concatenate the header and sequences into one line and seperate them by :

def concat(input, output):
        with open(input, "r") as f_input, open(output, "w") as f_output:
                lines = f_input.readlines()
                for n, line in enumerate(lines):
                        if line.startswith(">"):
                                lines[n] = line.rstrip()
                        else:
                                lines[n] = ":" + line
                f_output.write(''.join(lines))


concat("two_lines_seq.fa", "one_line_seq.fa")   # header and sequence in one line

# remove partial sequences

def remove(input, output):
        with open(input, "r") as f_input, open(output, "w") as f_output:
                lines = f_input.readlines()
                for line in lines:
                        if line.startswith(">"):
                                if "partial" not in line:
                                        f_output.write(line)


remove("one_line_seq.fa", "remove_partial_seq.fa")


# convert the file format back to fasta format

def fasta(input, output):
        with open(input, "r") as f_input, open(output, "w") as f_output:
                lines = f_input.readlines()
                for line in lines:
                        a = line.replace(":", "\n")
                        f_output.write(a)


fasta("remove_partial_seq.fa", "complete_seq.fa")


# tell user the partial sequences are removed

print("Partial protein sequences are removed, only complete sequences are kept for further analysis...")

cmd = "grep '>' complete_seq.fa | wc -l"
no_of_complete_seq = subprocess.check_output(cmd, shell=True).decode("utf-8")

no_of_partial_seq = int(no_of_seq) - int(no_of_complete_seq)

print(no_of_partial_seq, "partial sequences removed...")

print("Number of sequences left in the dataset:" + no_of_complete_seq)

print("All the complete protein sequences are saved in 'complete_seq.fa'")


# count the number of species

cmd = "grep '>' complete_seq.fa > header.txt"   # grep all the headers of the fasta file into a new file
os.system(cmd)

with open ("header.txt", "r") as file:
        lines = file.readlines()

species = set()
for line in lines:
        spe = re.findall(r'\[(.*?)\]', line)   # for each header, select the characters in the square bracket
        for item in spe:
                species.add(item)

no_of_species = len(species)


# evaluate the number of species

# ask user whether to continue with the dataset

def continue_or_not():
        user = input("Do you want to continue with the current dataset (yes/no)?\n")
        if user.lower() == 'yes':
                print("Of course, we will continue with the current dataset!")
                print("Total number of species:", no_of_species)
        elif user.lower() == 'no':
                print("Please re-enter the protein family and taxon ID")
                rerun_input()
                rerun_analysis()
        else:
                print("Please type yes or no")
                continue_or_not()


# define conditions in a if loop

while True:
        if no_of_species >= 10:   # if the number of species greater than or equal to 10, proceed
                print("Total number of species in the dataset:", no_of_species)
                break
        else:   # if there are less than 10 species, ask user whether to continue or resend query
                print("There are less than 10 species in your dataset")
                print("Total number of species in the dataset:", no_of_species)
                continue_or_not()
                break
