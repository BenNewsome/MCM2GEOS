#!/usr/bin/python

#Converts InChI or Smiles strings to PDB for use with molecule screen saver

import csv
from pybel import *
import shutil

#Open the file
Input_filename    ='GeosChem_Species.csv'
Output_folder   ='GeosChem_PDB/'
DEBUG             = True


def main():

   InChIs = get_list_of_InChIs()
   if DEBUG: print InChIs

   molecules = Convert_InChIs_to_pybel(InChIs)
   if DEBUG: print molecules
   
   molecules = Add_Hydrogens(molecules)

   print molecules[0].data   

   Write_pybel_to_PDB(molecules)

   print 'Written files to: ' + Output_folder  

   convert_to_proper_format()
   
   print 'Converted to correct format'

   return

def convert_to_proper_format():
   for filename in os.listdir(Output_folder):
      PDB_filename = Output_folder + filename
      TMP_filename       = Output_folder + 'tmp.tmp'
      PDB_file = open(PDB_filename, 'r')
      TMP_file = open(TMP_filename, 'w')
      new_file = ["TITLE     "+str(filename[:-4]) +"\n"]
      for line in PDB_file:
         
         if line.startswith("COMPND    UNNAMED"):
            line = "COMPND    "+filename[:-4] +"\n"
            new_file.append(line)
         elif line.startswith("HETATM"):
            line = line.replace("HETATM","ATOM  ")
            new_file.append(line)
         else:
            new_file.append(line)
      
      for line in new_file:
         TMP_file.write(line)

      PDB_file.close()
      TMP_file.close()

      shutil.move(TMP_filename, PDB_filename)

def get_list_of_InChIs():
   Input_file = open(Input_filename, 'rb')
   input_csv = csv.reader(Input_file)
   
   InChIs = []
   for row in input_csv:

      if (row[2].strip() == "") or (row[2].strip() == "InChI"): continue  

      else: 
         InChIs.append([row[0],row[2]])
      
       

      

   return InChIs;
      
def Add_Hydrogens(molecules):
   for molecule in molecules:
      molecule.make3D()
      molecule.localopt()
      molecule.title
   return molecules;

def Convert_InChIs_to_pybel(InChIs):
   molecules = []
   for InChI in InChIs:   
      molecule = readstring("inchi", InChI[1])
      molecule.data["Title"] = InChI[0]
      molecule.data["title"]  = InChI[0]
      molecule.data["Name"] = InChI[0]
      molecule.data["name"] = InChI[0]
      molecules.append(molecule)
#      print molecule.values()

   return molecules;

def Write_pybel_to_PDB(molecules):

   if not os.path.exists(Output_folder): 
      os.makedirs(Output_folder)
   
   
      

   for molecule in molecules:
      molecule_name     = molecule.data["Title"]
      Output_filename   = Output_folder + molecule_name + ".pdb"
      molecule.write('pdb', Output_filename, overwrite=True)

#      PDB_Output = Outputfile('pdb', Output_filename, overwrite=True)
#      PDB_Output.write(molecule)
#      PDB_Output.close()
   
   return;

main()
   
