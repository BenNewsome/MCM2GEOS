#!/usr/bin/python

# This program updates the csv provided by Andrew Rickard to include the functional groups.
# The functional groups are found using OpenBable
# The output format will be csv, but maybe also XML
# The Functional groups are currently extracted by SMILES strings, but InChI might be better?


import csv
from pybel import *

# Open the IO files
MCM_Inchis = open('MCMv3.2inchis.csv', 'rb')
Functional_Groups = open('Functional_groups.csv','wb')

# Accociate the IO files as CSV
reader = csv.reader(MCM_Inchis, )
writer = csv.writer(Functional_Groups)

# Read in the input CSV
species = []
for row in reader:
   species.append(row)

MCM_Inchis.close()



# Set the functional groups we want to look for
# These probably need checking


Ethyl = Smarts("[#6][#6]")
Aldehydes = Smarts("[CX3H1](=O)[#6]")
Carbonyl = Smarts("*C(=O)*")	# RC(=O)R







# Add the fuctional groups
First_line = True
for line in species:
   # Adds the titles in the first line
   if First_line:
      line.append('Ethyl')
      line.append('Aldehydes')
      line.append('Carbonyl')
      First_line = False
   else:
   # Check if Smiles string contains a functional group (Might replace with Inchi)
      print line[1]				# print the smiles string
#      mol = readstring("smi", line[1].strip())	# read the smiles string in smiles format
      mol = readstring("inc", line[1].strip())	# read the InChI string in smiles format
      line.append(len(Ethyl.findall(mol)))	# append the line with the number of ethyl groups
      line.append(len(Aldehydes.findall(mol)))	# '' '' aldehyde groups
      line.append(len(Carbonyl.findall(mol)))	# '' '' Carbonyl groups


print species

# Write out the output CSV
writer.writerows(species)

Functional_Groups.close()
