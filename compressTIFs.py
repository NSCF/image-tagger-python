## compress tiff images, and only tiff images...
## see https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#saving-tiff-images
## see https://havecamerawilltravel.com/tiff-image-compression/
## see also https://openpreservation.org/blogs/compression-at-your-discretion/


#IMPORTS
from PIL import Image, features
import os
from time import time, strftime, gmtime

#SETTINGS

method = 'tiff_adobe_deflate' #ZIP compression
#method = 'tiff_lzw' #LZW compression

#the directory with the images
image_dir = r'C:\temp\Herbarium mass digitization project\ImageTaggingExperiments'
overwrite = False #overwrite the existing files or write to a new location. If 'new_dir' is not specified below it will add to a subdirectory called 'compressed'
new_dir = r'C:\temp\Herbarium mass digitization project\ImageTaggingExperiments\pythonzipcompressed'

#SCRIPT
if not features.check('libtiff'):
  print('TIFF compression requires libtiff to be installed. Please run pip install libtiff and try again...')
  exit()

#function for creating human readable file sizes
#from https://stackoverflow.com/a/1094933/3210158
def sizeof_fmt(num, suffix="B"):
  for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Yi{suffix}"

#create the output directory if needed
if not overwrite:
  if len(new_dir):
    if not os.path.isdir(new_dir):
      try:
        os.mkdir(new_dir)
      except:
        print('Please provide a valid output directory...') #the input string must not have been valid
        exit()
  else:
    new_dir = os.path.join(image_dir, 'compressed')
    if not os.path.isdir(new_dir):
      try:
        os.mkdir(new_dir)
      except:
        print('Eish! Something went wront with creating the \'compressed\' directory...') #the input string must not have been valid
        exit()

print('Starting to compress images')

start = time()
count = 0
originalsize = 0
finalsize = 0

with os.scandir(image_dir) as it:
  for entry in it:
    if entry.is_file():
      originalsize += entry.stat().st_size
      file = entry.name
      if file.endswith('.tif'):
        infile = os.path.join(image_dir, file)
        outfile = os.path.join(new_dir, file)

        if not overwrite:
          if os.path.exists(outfile):
            continue

        try:
          with Image.open(infile) as im:
            im.save(outfile, compression = method)
            finalsize += os.path.getsize(outfile)
            count += 1
        except Exception as e:
          message = f'cannot convert {infile}: {e}'
          print(message)

end = time()
print('Finished compressing files')
totaltime = strftime("%H:%M:%S", gmtime(end - start))
print(count, 'images compressed in', totaltime)
print('Total original size:', sizeof_fmt(originalsize))
print('Total compressed size:', sizeof_fmt(finalsize))

