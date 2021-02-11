import os
import glob
import pandas as pd
os.chdir(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\PODATKI")

extension = 'csv'
all_filenames_knjige = [i for i in glob.glob('knjige*.{}'.format(extension))] 
all_filenames_zanri = [i for i in glob.glob('zanri*.{}'.format(extension))] 
all_filenames_nagrade = [i for i in glob.glob('nagrade*.{}'.format(extension))] 

#KNJIGE
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames_knjige ])
#export to csv
combined_csv.to_csv( "zdruzene_knjige.csv", index=False, encoding='utf-8-sig')

#ZANRI
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames_zanri ])
#export to csv
combined_csv.to_csv( "zdruzeni_zanri.csv", index=False, encoding='utf-8-sig')

#NAGRADE
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames_nagrade ])
#export to csv
combined_csv.to_csv( "zdruzene_nagrade.csv", index=False, encoding='utf-8-sig')