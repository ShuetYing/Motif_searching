# python program to perform motif searching of protein of interest 
# To run the program, there is a script named ‘execute_program.sh’ which contains codes needed to run the scripts. 
# To execute the program, type ./execute_program.sh in the server.


Step 1: key in the protein family and taxonomic ID of the taxonomic group of interest
The protein family and taxon ID keyed in are used to create query to obtain protein sequences
from the ncbi database. 
o protein family
 key in the protein family in the program twice
o taxon ID
 key in the taxon ID
 please key in an integer, do not include ‘txid’
o ncbi database
 all the protein sequences from the database are saved in a file named ‘raw_sequences.fa’


Step 2: filter result – user decide whether to use the obtained sequences
The program counts the number of sequences obtained from the database and determine whether to continue with the dataset or give user 
the option to choose. After assessing the number of sequences, the program counts the number of species in the dataset and determine 
whether to continue.
o number of sequences 
 too much (difficult to process data) or too few (might not provide useful information) sequences from the query: option to continue or not
 please type yes or no (without space before, after or in between)
 no result from the query: please re-enter protein family and taxon ID
o remove partial protein sequences
 complete protein sequences are saved in file named ‘complete_seq.fa’
o number of species
 more than 10 species: have enough information to proceed
 less than 10 species (might not provide useful information): option to continue or resend query, please type yes or no 
  (without space before, after or in between) 


Step 3: filter result – user has the options to filter sequences and species
The program returns the number of sequences and the number of species to the user. 
User has the options to choose the number of sequences and the species continue for analysis.
o number of sequences
 2 < number of sequences < 600: proceed with the analysis
 number of sequences < 2 (unable to perform multiple sequence alignment with only one sequence): please re-enter protein family and taxon ID
 number of sequences > 600 (conservation plot might be difficult to read): option to continue or not, please type yes or no (without space before, after or in between)
 if not continuing, there are two options, please type 1 or 2 (without space before or after)
 1 : enter an integer between 2 and 600 and the program will pick the top sequences from the current sequence set
 2 : resend query, please re-enter protein family and taxon ID
o species
 option whether to choose interested species or continue with all, please type yes or no (without space before, after or in between)
 if choose species of interest, please enter all the index number of your interested species from the given list
 please include a space in between every index number (without space before the first number and after the last number)
 please type yes or no (without space before, after or in between) when asked to confirm the selected species of interest


Step 4: multiple sequence alignment
o perform multiple sequence alignment
 sequence of interest from the previous step is used as input
o multiple sequence alignment result is saved in afile named ‘MSA.aln’,the result is used to plot conservation plot between sequences


Step 5: conservation plot
User will be asked to provide the window size used for plotting. 
The program plots the conservation plot and display it before calculating the level of similarity of the sequence data set.
o specify window size used to plot the conservation plot
 window size is the length that used to compare across sequences
 please enter an integer
 plot will be shown (x-axis: residual position, y-axis: similarity)
 option to change the window size, please type yes or no (without space before, after or in between)
o degree of similarity within sequences
 the level of similarity will be given
 higher similarity which is highly conserved sequence might indicate higher chance of finding common motif between all the sequences
 the position of residual with highest similarity will also be given   
 more specific information of the multiple sequence alignment such as the number of identical and similar residual in each sequence is provided in a file named ‘MSA_info.txt’


Step 6: scan protein against PROSITE database to find motif
Scan each protein sequences against the database to determine associated motif. 
The program counts the number of occurrences of motif in the sequences to give information on the most common motif found in the protein sequences.
o output of motif
 information on whether all sequences have motif found in the database will be given
 if not, the number of sequences with associated motif will be given
o number of occurrences of each found motif
 a table containing the motif name and number of occurrences in the sequence set where the motifs are arranged in a descending order in terms of number of occurrences
o option to view more detailed information of the motifs
 please type yes or no (without space before, after or in between)
 if there are motif of interest, please type in the motif name one at a time
 the motif information is saved in a file named ‘motif_info.csv’

     
Step 7: find potential antigenic region in the protein sequences – useful for immunology Scan protein sequences and predict antigenic region.
Information of antigenic region is saved in file named ‘Ag_info.csv’ if interested.


Step 8: identify HTH motif in protein sequences which might suggest protein function
Scan protein sequences and identify presence of HTH motif in the protein sequences. 
The program gives information on whether there is HTH motif identified.
o number of HTH motif identified
 information of HTH motif is saved in ‘binding_motif_info.csv’
 
