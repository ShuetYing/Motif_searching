#!/usr/bin/python3

import os, subprocess, sys


# rerun the input script

def rerun_input():
        exec(open('user_input.py').read())


# rerun analysis of protein sequences

def rerun_analysis():
        exec(open('prot_seq.py').read())


# rerun script to allow user to make option

def rerun_option():
        exec(open('user_option.py').read())


# tell user there are how many sequences

cmd = "grep '>' complete_seq.fa | wc -l"
no_of_seq = subprocess.check_output(cmd, shell=True).decode("utf-8")
print("Total number of sequences in the current dataset is", no_of_seq)


# allow user to decide how many sequences to keep

while True:
        if 2 < int(no_of_seq) < 600:   # if number of sequences is between 2 and 600, include all the sequences as input for the next step
                print("Let's continue with the analysis!")
                with open("remove_partial_seq.fa", "r") as f_input, open("seq_wanted.fa", "w") as f_output:   # write the sequences into seq_wanted.fa
                        content = f_input.readlines()
                        for line in content:
                                f_output.write(line)
                break
        elif int(no_of_seq) < 2:   # if there is only one sequences, ask user to resend query
                print("Sorry, there is only one sequence, we can't continue...\nPlease make a new query!")
                rerun_input()
                rerun_analysis()
                rerun_option()
                break
        else:   # if there are more than 600 sequences, ask user whether to continue
                print("There are more than 600 sequences in your dataset, it might be difficult for analysis...")
                user_input = input("Do you want to continue with the current dataset (yes or no)?\n")
                          if user_input.lower() == "yes":
                        print("OK!")
                        with open("remove_partial_seq.fa", "r") as f_input, open("seq_wanted.fa", "w") as f_output:   # write the sequences into seq_wanted.fa
                                content = f_input.readlines()
                                for line in content:
                                        f_output.write(line)
                        break
                elif user_input.lower() == "no":
                        user = input("Do you want to choose the number of sequences to continue or resend query?\nType 1 to select the number of sequences to continue with\nType 2 to resend query\n")   # let user choose to pick the number of sequence or resend query
                        if user == "1":   # pick number of sequences
                                num = input("Please enter the number of sequences you want to continue with...(please enter an integer between 2 to 600)\n")
                                list = list(range(0, int(num)))
                                with open("remove_partial_seq.fa", "r") as f_input, open("seq_wanted.fa", "w") as f_output:   # write the number of sequences user want into seq_wanted.fa
                                        content = f_input.readlines()
                                        for n in list:
                                                for number, line in enumerate(content, start=0):
                                                        if n == number:
                                                                f_output.write(line)
                                break
                        elif user == "2":   # resend query
                                rerun_input()
                                rerun_analysis()
                                rerun_option()
                                break
                        else:
                                print("Please type 1 to select the number of sequences or 2 to resend query!")
                else:
                        print("Please type yes or no!")


# build a dictionary to store the sequence header and protein sequence

fasta = {}   # an empty dictionary

with open("two_lines_seq.fa") as file:
        for line in file:
                line = line.strip()
                if not line:
                        continue
                if line.startswith(">"):
                        seq_name = line[1:]
                        if seq_name not in fasta:
                                fasta[seq_name] = []
                        continue
                seq = line
                fasta[seq_name].append(seq)


# show user the header which contain the id, organism name and index position

dict = list(fasta)
keys = list(fasta.keys())


# allow user to choose the organism of interest

while True:
        user_input = input("Do you want to choose the organism to proceed with (yes or no)?\n")
        if user_input.lower() == "yes":
                for keys in dict:
                        print('header: {}, index: {}'.format(keys, dict.index(keys)))
                species = input("Please enter the index number for the species of interest:\n")
                index = species.split()
                index = list(map(int, index))
                print("Please see the selected index:\nindex: ", index)
                confirm = input("Please confirm that the selected index is correct (yes or no):\n")
                if confirm.lower() == "yes":
                        print("OK! Let's continue...")
                        with open("remove_partial_seq.fa", "r") as f_input, open("seq_wanted2.fa", "w") as f_output:   # copy the sequences of organism that user are interested in into seq_wanted2.fa
                                content = f_input.readlines()
                                for n in index:
                                        for number, line in enumerate(content, start=0):
                                                if n == number:
                                                        f_output.write(line)
                        break
                elif confirm.lower() == "no":
                        print("Let's choose again!")
                else:
                        print("Please type yes or no!")
        elif user_input.lower() == "no":
                print("OK! Let's continue...")
                with open("seq_wanted.fa", "r") as f_input, open("seq_wanted2.fa", "w") as f_output:   # copy the sequences user choose from the previous step into seq_wanted2.fa
                        content = f_input.readlines()
                        for line in content:
                                f_output.write(line)
                break
        else:
                print("Please type yes or no!")


# merge the files containing the sequences that user are interested in

with open("seq_wanted.fa") as file:
        data1 = file.read()

with open("seq_wanted2.fa") as file:
        data2 = file.read()

data1 += data2

with open("merged_option.fa", "w") as file:
        file.write(data1)


# remove the repeated sequences

repeat = set()
f_output = open("interested_sequences.fa", "w")
for line in open("merged_option.fa", "r"):
        if line not in repeat:
                f_output.write(line)
                repeat.add(line)

f_output.close()


# change the format of the file where the header and sequence are in different line so that it can be used as input for next step

def fasta(input, output):
        with open(input, "r") as f_input, open(output, "w") as f_output:
                lines = f_input.readlines()
                for line in lines:
                        a = line.replace(":", "\n")
                        f_output.write(a)


fasta("interested_sequences.fa", "interested_seq.fa")

print("The protein sequences of interest are saved in 'interested_seq.fa' fasta file")
