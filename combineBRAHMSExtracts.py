import csv, os
from queue import Empty

filepath = r'C:\general work\NSCF\TypeTagging'
files = [
    r'PRE_Types_BODATSA_July_2022-OpenRefine.csv',
    r'PRE_NonTypes_BODATSA_Aug_2022_OpenRefine.csv',
    r'PRE_NonTypes_BODATSA_Aug_2022_2_OpenRefine.csv'
]

writefilename = r'PRE_Types&NonTypes_BODATSA_Aug_2022_combined.csv'

fields = ['BARCODE', 'FULLNAME', 'HOMETYPE', 'HOMETSTAT', 'CONTINENT', 'COUNTRY', 'MAJORAREA', 'FAMILY', 'GENUS', 'SPECIES', 'COLLECTOR LASTNAME', 'ACCEPTEDGENUS', 'ACCEPTEDSPECIES']


#SCRIPT

allrecords = []

for file in files:
    fullpath = os.path.join(filepath, file)
    with open(fullpath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:

            #drop unwanted fields
            keys = list(record.keys())
            for key in keys:
                if key not in fields:
                    del record[key]

            #add additonal fields
            if 'HOMETSTAT' not in record:
                record['HOMETSTAT'] = None

            if record['HOMETYPE'] is None or record['HOMETYPE'].strip() == '':
                record['CAPTION'] = record['FULLNAME']
            else:
                record['CAPTION'] = record['HOMETYPE'].strip()

            #add to list
            allrecords.append(record)

#write out results
with open(os.path.join(filepath, writefilename), 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerows(allrecords)

print('All done, thank you, bye bye...')
