# generate the csv file to join to the specimen records
# add views from filenames

import os 
import csv
import re
import pandas as pd

### SETTINGS

datafile_dir = r''
datafile = r''
image_catnum_field = '' # the field in the dataset that has catalog numbers formatted to match those in the file name - the joining field.

keyword_fields = [
  'country',
  'species',
  'typestatus'
]

image_dir = r'G:\PRE' # the folder with the images; does not include subfolders
outputfile = r'Iziko-mammals-types-2023.csv' # 
fileext = '.tif'

# THE SCRIPT

structures = {
  'H': 'head',
  'S': 'skin',
  'L': 'skull',
  'C': 'cranium',
  'M': 'mandible',
  'P': 'postcranium',
  'K': 'skeleton',
  'W': 'whole specimen'
}

sides = {
  'L': 'left',
  'R': 'right',
}

views = {
  'D': 'dorsal',
  'V': 'ventral',
  'L': 'lateral',
  'O': 'occlusional',
  'C': 'occipital',
  'A': 'anterior',
  'P': 'posterior',
  'R': 'proximal',
  'S': 'distal',
  'M': 'medial',
  'U': 'unspecified'
}

descriptors = {
'G': 'group', 
'V': 'view', 
'S': 'section', 
'I': 'image'
}

def make_view(code):
  '''make a full view description from the code'''
  if code and code.strip():
    code = code.upper().strip()
    view = []

    if code == "LABEL":
      view.append('label')
    elif len(code) == 3: #we have a side
      try:
        view.append(structures[code[0]])
        view.append(sides[code[1]])
        view.append(views[code[2]])
      except:
        raise Exception('invalid code')
    elif len(code) == 2:
      if any(char.isdigit() for char in code):
        try:
          view.append(descriptors[code[0]])
          view.append(re.search(r'\d+', code)[0])
        except:
          raise Exception('invalid code')
      else:

        try:
          view.append(structures[code[0]])
          view.append(views[code[1]])
        except:
          raise Exception('invalid code')
    elif len(code) == 1:
      try:
        view.append(structures[code[0]])
      except:
        raise Exception('invalid code')

    else:
      raise Exception('invalid code')

    return ' '.join(view).strip()


print('reading image directory')
try:
  images = os.listdir(image_dir)
except Exception as ex:
  print('Opps! ' + str(ex))
  exit()

images = list(filter(lambda x: x.lower().endswith(fileext.lower()), images))

print('reading data file...')
fullpath = os.path.join(datafile_dir, datafile)
try: 
  df = pd.read_csv(fullpath, na_values=['', ' '], keep_default_na=False)
except Exception as e:
  print(e)
  print('Quitting...')
  exit()

if df.empty:
  print('No records found in', datafile)
  print('Quitting...')
  exit()

print(df.shape[0], 'records read from', datafile)   
try: 
  df = df.set_index(image_catnum_field, drop = False, verify_integrity = True)
except ValueError:
  print('There are duplicate values in the field \'', image_catnum_field + '\'')
  print('Please remove the duplicates and try again.')
  print('Quitting...')
  exit()

#check the file includes all the fields
missingfields = []
for field in keyword_fields:
    if field not in df:
        missingfields.append(field)

if len(missingfields) > 0:
    print('The following keyword fields are not in the dataset. Check spelling, case, and fix the dataset if needed:')
    print(' | '.join(missingfields))
    exit()

print('making image tags dataset')
rows = []
missing = set()
code_errors = set()
for image in images:
  
  catalognumber = image.split('_')[0]

  row = {
    "filename": image,
    "views": []
  }

  parts = re.split(r"[_\.]", image)
  parts.pop()
  parts = parts[1:]
  has_code_errors =  False
  for part in parts:
    
    try:
      view =  make_view(part)
    except:
      code_errors.add(image)
      has_code_errors = True
      continue
    
    if view:
      row["views"].append(view)
  
  if has_code_errors:
    continue

  row["views"] = ','.join(row['views'])

  data_record = None
  try:
    data_record = df.loc[catalognumber]
  except: #it can only be a key error
    missing.add(catalognumber)
    continue


  for keyword_field in keyword_fields:
    keyword_value = data_record[keyword_field]
    if pd.isna(keyword_value):
      keyword_value = None
    row[keyword_field] = keyword_value

  rows.append(row)

if len(rows):
  print('saving image dataset file with', len(rows), 'records')
  with open(os.path.join(image_dir, outputfile), 'w', encoding='UTF8', newline='', errors='ignore') as f:
    fields = ['filename', 'views', *keyword_fields]
    dict_writer = csv.DictWriter(f, fields)
    dict_writer.writeheader()
    dict_writer.writerows(rows)

  if len(missing):
    print("The following specimens are not in the data file:")
    for num in missing:
      print(num)

  if len(code_errors):
    print("The following images have code errors:")
    for image in code_errors:
      print(image)
else:
  if len(code_errors):
    print("The following images have code errors:")
    for image in code_errors:
      print(image)
  else:
    print("no images matched records in the dataset")

print('All done, bye bye now...')