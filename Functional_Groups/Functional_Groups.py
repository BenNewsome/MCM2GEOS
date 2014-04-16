#!/usr/bin/python

# This program updates the csv provided by Andrew Rickard to include the functional groups.
# The functional groups are found using OpenBable
# The output format will be csv, but maybe also XML
# The Functional groups are currently extracted by SMILES strings, but InChI might be better?


import csv
from pybel import *

# Open the IO files
# Change the inputs here

#Input_InChI = open('MCMv3.2inchis.csv', 'rb')
#Functional_Groups = open('Functional_groups.csv','wb')
#Webpage = 'MCM_deposition'

Input_InChI = open('GeosChem_Species.csv', 'rb')
Functional_Groups = open('GEOS_groups.csv','wb')
Webpage = 'GEOS_depostion'

# Specify the column that the inchis are provided in
InChI_Column = 3

# Python starts counting at 0 so take 1
InChI_Column = InChI_Column - 1



# Accociate the IO files as CSV

reader = csv.reader(Input_InChI, )
writer = csv.writer(Functional_Groups)

# Read in the input CSV
species = []
for row in reader:
   species.append(row)

Input_InChI.close()



# Set the functional groups we want to look for
# These probably need checking


Ethyl = Smarts("[#6][#6]")
Aldehydes = Smarts("[CX3H1](=O)[#6]")
Carbonyl = Smarts("*C(=O)*")	# RC(=O)R
Peroxide = Smarts("*OO")	# R-O-O-H
Pan = Smarts("*C(=O)OON(=O)=O")	#peroxyacetylnitrate




Blank_Line=""


# Add the fuctional groups
First_line = True
for line in species:
   # Adds the titles in the first line
   if First_line:
      line.append('Ethyl')
      line.append('Aldehydes')
      line.append('Carbonyl')
      line.append('Peroxide')
      line.append('Pan')
      First_line = False
   else:
      if not (line[InChI_Column].strip() == Blank_Line):
 
      # Check if Smiles string contains a functional group (Might replace with Inchi)
         mol = readstring("inchi", line[InChI_Column].strip())	# read the InChI string in smiles format
         line.append(len(Ethyl.findall(mol)))	# append the line with the number of ethyl groups
         line.append(len(Aldehydes.findall(mol)))	# '' '' aldehyde groups
         line.append(len(Carbonyl.findall(mol)))	# '' '' Carbonyl groups
         line.append(len(Peroxide.findall(mol)))	# '' '' Peroxide groups
         line.append(len(Pan.findall(mol)))	# '' '' Pan groups
      else:
         line.append(Blank_Line)  
         line.append(Blank_Line)  
         line.append(Blank_Line)  
         line.append(Blank_Line)  
         line.append(Blank_Line)  

print('CVS written') 

# Write out the output CSV
writer.writerows(species)

Functional_Groups.close()

#This bit writes out a HTML file and all the images.
if not os.path.exists('web'):
   os.makedirs('web')


html = open('web/'+Webpage+'.html','wb')


print('Writing the HTML file')
#write the header
html.write('''

<!DOCTYPE html>
<html>
<body>

<table style="width:300px">

''')

#Write the content
for line in species:
  html.write( 
  '<tr>' +	
    '<td>'+str(line[0])+'</td>'+
    '<td>'+str(line[1])+'</td>'+	
    '<td>'+str(line[2])+'</td>'+
    '<td>'+str(line[3])+'</td>'+
    '<td>'+str(line[4])+'</td>'+
    '<td>'+str(line[5])+'</td>'+
    '<td>'+str(line[6])+'</td>'+
    '<td>'+str(line[7])+'</td>'+
    '<td>'+str(line[8])+'</td>'+
    '<td>'+'<img width="100" height="100" src="img/'+str(line[0])+'.png" alt="'+str(line[0])+'">'+'</td>'+
  '</tr>'
  )


#Write the end
html.write('''
</table>

</body>
</html>

''')

print('HTML file written')

print('Creating the pngs')

if not os.path.exists('web/img/'):
   os.makedirs('web/img/')

Firstline=True
a=0
for line in species:
  if Firstline:
    Firstline=False
  else:
    if not (line[InChI_Column].strip() == Blank_Line): #Make sure the line isn't blank
      print('Writing out the png')
      mol = readstring("inchi", line[2].strip())	# read the InChI string in smiles format
      img_filename = 'web/img/' + line[0] + '.png'
      mol.draw(show=False, filename=img_filename )
      a=a+1
      if a==200:
        exit()




