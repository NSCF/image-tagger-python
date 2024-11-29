# get a list of unique catalog numbers from a set of image files in a directory
# assumes that an underscore is always used to separate the catalog number from the rest of the file name
import os

image_dir = r'D:\Type specimen imaging\Ditsong National Museum of Natural History\Ditsong Paleontology\TIFF'
file_ext = '.tif'

print('reading image directory')
try:
  dir_contents = os.listdir(image_dir) #get a list of everything in dir
except Exception as ex:
  print('Oops! ' + str(ex)) # we only land here if something went wrong...
  exit()

images = list(filter(lambda x: x.lower().endswith(file_ext.lower()), dir_contents)) # filter dir_contents any anything that ends with our file extension (we make it lowercase so that case doesn't matter)

if len(images) == 0:
  print('There are files of type', file_ext, 'in your directory')
  exit()

cat_nums = set() # remember from high school maths that a mathematical set only has unique values
for image in images:
  cat_num = image.split('_')[0] # split the file name on underscores and just keep the first (index 0) bit
  cat_nums.add(cat_num) # add the cat num to the set

if len(cat_nums) > 0:
  cat_nums = list(cat_nums) # convert catnums from a set to a list
  cat_nums.sort() # sort the list
  for cat_num in cat_nums:
    print(cat_num)
  print() # print a blank line
  print('All done...')
else:
  print('It looks like something went wrong, there are no catalog numbers...')