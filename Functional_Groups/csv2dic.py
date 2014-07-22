import csv
from pybel import *


Input_filename    ='GeosChem_Species.csv'
Output_filename   ='Species.csv'
debug             = True

def main():


   input_file  = open(Input_filename, 'rb')
   input_csv   = csv.reader(input_file)

   output_file = open(Output_filename, 'wb')
   output_csv  = csv.writer(output_file)



   for row in input_csv:

      if    (row[2].strip() == "InChI"):
         new_row = ["Name", "Formula", "InChI", "smiles", "RMM", "Latex"]
         output_csv.writerow(new_row)
      else: 
         Name = row[0]
         Formula = row[1]
         InChI   = row[2]
         smiles  = get_smiles(row[2])
         RMM     = get_RMM(row[2])
         Latex   = get_latex(row[0])
   
         new_row = [Name, Formula, InChI, smiles, RMM, Latex]
         output_csv.writerow(new_row)

   print "Complete. CSV written to " + str(Output_filename)
         

def get_smiles(InChI):
   if (InChI == ""):
      smiles =  ""
   else:
      if debug: print InChI
      molecule = readstring("inchi", InChI)
      smiles   = str(molecule.write(format='smi'))
      if debug: print smiles
   return smiles;

def get_RMM(InChI):
   if (InChI == ""):
      mass = ""
   else:
      molecule = readstring("inchi", InChI)
      mass     = molecule.exactmass
      if debug: print mass
   return mass;

def get_latex(name):

   dictionary = {'O3':'O_3'}

   if name in dictionary:
      latex = dictionary[name]
   else:
      latex = ""

   return latex;


main()

