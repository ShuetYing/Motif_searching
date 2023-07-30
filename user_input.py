#!/usr/bin/python3

import os, sys

# get the protein family of interest from the user

while True:
        family = input("Please enter the protein family of interest:\n")
        retype_family = input("Please retype the protein family of interest:\n")
        if family == retype_family:
                protein = family
                break
        else:
                print("Protein family doesn't match. Please try again!")


# get the taxon ID from the user

while True:
        try:
                id = "txid" + str(int(input("Please enter the taxon ID for the taxonomic group of interest:\n")))
                break
        except ValueError:
                print("It's not an integer. Please try again!")


# get the protein sequences from ncbi database

print("Please wait patiently, searching protein sequences from the database...")

cmd = "esearch -db protein -query '" + protein + "[PROT] AND " + id + "[ORGN]' | efetch -format fasta > raw_sequences.fa"

os.system(cmd)


# tell user where the result is stored

print("The result containing sequences from the database is saved in 'raw_sequences.fa'")
