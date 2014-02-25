#!/usr/share/anaconda/bin/python

# Program summary

# Strip the windows newline ^M

# remove the first blank ignore

# Fix the misplaced ';' (Equations not going to anything)

# Add the DEFFIX variables 

# Import required modules
import os
import glob
import re
import argparse
from subprocess import call





def main():
#Read in the arguments


   

   parser = argparse.ArgumentParser(description='This creates KPP folders from a MCM.kpp file.')
   parser.add_argument('-i', '--input', help='Input .kpp file', required=True)
   parser.add_argument('-o', '--output', help='Output folder name', required=True)
   parser.add_argument('-m', '--manual_kpp', help='Chose Manual kpp generation', required=False)
   args = parser.parse_args()

   if args['manual_kpp'].lower() == 'true' :
      exicure_kpp_manualy = True

# Show the arguments
   print ("Input file is '" + args.input + "'")
   print ("Output folder is'" + args.output + "'" )

# Use the arguments
   input_file = args.input
   output_folder = args.output
   if not os.path.exists(output_folder):
      os.makedirs(output_folder)

   gckpp = os.path.join(output_folder, 'gckpp.kpp') 


# Open the kpp file to fix
   f1 = open(input_file, 'rb')
   f2 = open(gckpp, 'wb')

# Start scanning the document

   for line in f1:
# Strip the windows newline
      line = line.replace('\r','')

# Replace the first blank ignore with O2
      if line.startswith(' ='):
         print 'Old line is "' + str(line) + "'"
         line = line.replace(' =','O2 =')
         print 'New line is "' + str(line) + "'"

# Fix the O + O3 equation
      if 'O + O3 = :' in line:
         print 'Old line is "' + str(line) + "'"
         line = line.replace('O + O3 = :','O + O3 = O2 :')
         print 'New line is "' + str(line) + "'"

# #Fix the OH + HO2 equation
      if 'OH + HO2 = :' in line:
         print 'Old line is "' + str(line) + "'"
         line = line.replace('OH + HO2 = :','OH + HO2 = H2O + O2 :')
         print 'New line is "' + str(line) + "'"

# Add the DEFFIX
      if line.startswith('#INCLUDE atoms'):
         print 'Old line is "' + str(line) + "'"
         line = (str(line) + '\n' + \
         '\n' + \
         '#DEFFIX' + '\n' +
         'EMISSION        =          IGNORE;' + '\n' +
#      'H2              =          IGNORE;' + '\n' +
         'N2              =          IGNORE;' + '\n' +
#      'O2              =          IGNORE;' + '\n' +
         'H2O             =          IGNORE;' + '\n' +
         'DRYDEP          =          IGNORE;' + '\n' +
         '\n')    
         print 'New line is "' + str(line) + "'"


# Write the updated line   
      f2.write(line)

# Close the files
   f1.close()
   f2.close()

# Call kpp with the new file
   print "Calling KPP"

# Decend into the folder containing gckpp.kpp
# This might change later if we want everything in one folder.
   os.chdir(output_folder)
   print os.path.abspath(__file__)



# Create a option to do manual kpp calls due to buggs with kpp in testing.
   if not exicute_kpp_manualy:
# Does a system call for kpp
      try:
         kpp.check_call(["kpp", "gckpp.kpp"]) # Default kpp curently not working - see diff
      except kpp.CalledProcessError:
         pass # Errors in KPP
      except OSError:
         pass # KPP not found

      print "KPP files generated"
   
   else:
      print 'manual kpp generation chosen. Expect errors now.'



   print "Changing files from .f to .F90"

# Change the generated filetypes from .f to .F90
   files_to_change = '*.f'
   old_end='.f'
   new_end='.F90'


   for filename in glob.glob(files_to_change):
      newfile = filename
      newfile = newfile.replace(old_end, new_end)
      os.rename(filename, newfile)

   print 'Files renamed'

# Parse gckpp_rates.F90 to change photolosys rates.
# J in MCM to PHOTOL in geos

   print 'Updating the Photolasis rates'


# Check if file is here first
   if not os.path.exists('gckpp_Rates.F90'):
      print 'gckpp_Rates.F90 was not created for some reason \n Exiting'
      exit(1)
   gckpp_Rates_old = open('gckpp_Rates.F90', 'r')
   gckpp_Rates_new = open('gckpp_Rates_new.F90', 'w')

   Photol_Conversion = Get_Photol_Dictionary()

   print Photol_Conversion.keys()

   In_The_Rates = False
   for line in gckpp_Rates_old:
# If in the Subroutine Update_Rconst then translate
      Trimmed_Line = line.lstrip()

      if Trimmed_Line.startswith('SUBROUTINE Update_RCONST'):
         In_The_Rates = True

      if line.startswith('END SUBROUTINE Update_RCONST'):
         In_The_Rates = False

      if In_The_Rates:
         for Key in Photol_Conversion.keys():
            if Key in line:
               line = line.replace(Key, Photol_Conversion[Key])
               print line
         Update_Photol(line, Photol_Conversion)
         
      gckpp_Rates_new.write(line)      

   gckpp_Rates_new.close()

# #Need to repalce the old file with the new one
   print '~~~The new file still needs to replace the old one!!!!!~~~'


   print 'Photolasys rates updated'

   os.chdir('../')

# Assend back into the origional directory - might change later


   print "Script Complete"


# END OF MAIN PROGRAM





# Defined functions

def Update_Photol(text, Photol_Conversion):
   for key in Photol_Conversion.items():
      text = text.replace(*key)      
   return text

# Photol conversion Dictionary
# This should be put into a module
def Get_Photol_Dictionary():
   Photol_Conversion = {
      'J(1)'   :  'PHOTOL(1)',
      'J(2)'   :  'PHOTOL(1)',
      'J(3)'   :  'PHOTOL(1)',
      'J(4)'   :  'PHOTOL(1)',
      'J(5)'   :  'PHOTOL(1)',
      'J(6)'   :  'PHOTOL(1)',
      'J(7)'   :  'PHOTOL(1)',
      'J(8)'   :  'PHOTOL(1)',   
      'J(9)'   :  'PHOTOL(1)',
      'J(10)'   :  'PHOTOL(1)',
      'J(11)'   :  'PHOTOL(1)',
      'J(12)'   :  'PHOTOL(1)',
      'J(13)'   :  'PHOTOL(1)',
      'J(14)'   :  'PHOTOL(1)',
      'J(15)'   :  'PHOTOL(1)',
      'J(16)'   :  'PHOTOL(1)',
      'J(17)'   :  'PHOTOL(1)',
      'J(18)'   :  'PHOTOL(1)',   
      'J(19)'   :  'PHOTOL(1)',
      'J(20)'   :  'PHOTOL(1)',
      'J(21)'   :  'PHOTOL(1)',
      'J(22)'   :  'PHOTOL(1)',
      'J(23)'   :  'PHOTOL(1)',
      'J(24)'   :  'PHOTOL(1)',
      'J(25)'   :  'PHOTOL(1)',
      'J(26)'   :  'PHOTOL(1)',
      'J(27)'   :  'PHOTOL(1)',
      'J(28)'   :  'PHOTOL(1)',   
      'J(29)'   :  'PHOTOL(1)',
      'J(30)'   :  'PHOTOL(1)',
      'J(31)'   :  'PHOTOL(1)',
      'J(32)'   :  'PHOTOL(1)',
      'J(33)'   :  'PHOTOL(1)',
      'J(34)'   :  'PHOTOL(1)',
      'J(35)'   :  'PHOTOL(1)',
      'J(36)'   :  'PHOTOL(1)',
      'J(37)'   :  'PHOTOL(1)',
      'J(38)'   :  'PHOTOL(1)',   
      'J(39)'   :  'PHOTOL(1)',
      'J(40)'   :  'PHOTOL(1)'}
   
   return Photol_Conversion


if __name__ == '__main__':
   main()
