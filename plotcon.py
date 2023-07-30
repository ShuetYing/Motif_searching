#!/usr/bin/python3

import os, sys

# perform multiple sequence alignment between sequences

print("Performing multiple sequence alignment...")

cmd = "clustalo -i interested_seq.fa -o MSA.fa -v"

os.system(cmd)


# perform MSA and generate result that is more readable

cmd = "clustalo -i interested_seq.fa -o MSA.aln --outfmt=clustal --wrap=80 --force"

os.system(cmd)

print("The result of multiple sequence alignment is saved in 'MSA.aln'")


# ask user to input the window size used for plotting

while True:
        try:
                window_size = str(int(input("Please specify the window size (window of comparison) used for plotting:\n")))
                print("window size = ", window_size)
                break
        except ValueError:
                print("Please enter an integer!")


# plot sequence conservation between sequences

cmd = "plotcon MSA.fa -winsize " + window_size + " -graph png"

os.system(cmd)


# display the plot to user

import PIL
from PIL import Image
img = Image.open('plotcon.1.png')
img.show()

print("Hmmm, it might take a while to load the image, please be patient...")

# create a function which ask user for window size input, plot and show image

def rerun_size():
        exec(open('winsize_input.py').read())


# ask user whether to change the parameter

while True:
        change_size = input("Do you want to change the window size (yes or no)?\n")
        if change_size.lower() == "yes":
                rerun_size()
        elif change_size.lower() == "no":
                print("OK! We'll continue with the current plot to provide the level of similarity.")
                break
        else:
                print("Please type yes or no!")


# get the level of similarity of the sequences

cmd = "plotcon MSA.fa -winsize " + window_size + " -graph data"

os.system(cmd)


# extract only the data, remove the comments

cmd = "grep -v '##' plotcon1.dat > plotcon1.txt"

os.system(cmd)


# assess the degree of similarity between sequences

with open("plotcon1.txt", "r") as file:   # file contains similarity at each residual position
        no_of_residual = len(file.readlines())

simi = []   # store similarity
posi = []   # store residual position
with open("plotcon1.txt") as file:
        for line in file.readlines():
                pos, sim = line.split('\t')
                posi.append(pos)   # position of each residual
                simi.append(sim)   # similarity of the residual

similarity = []
for x in simi:
        similarity.append(float(x.replace("\n", "")))

position = []
for x in posi:
        position.append(int(float(x)))

total = position[-1]

level_of_similarity = round(sum(similarity)/total,8)

print("The degree of similarity within the sequence set is " + str(level_of_similarity))

print("The similarity of each residual position is saved in 'plotcon1.txt'")


# tell user which residual has the highest similarity between the sequences

max_value = max(similarity)

index = similarity.index(max_value)

print("Residual at position ", index+1, " in the alignment has the highest similarity which is", max_value)


# provide user the information of the multiple seuqence alignment result

cmd = "infoalign MSA.fa MSA_info.txt -nousa"

os.system(cmd)

print("More information on the multiple sequence alignement result is saved in 'MSA_info.txt'")
