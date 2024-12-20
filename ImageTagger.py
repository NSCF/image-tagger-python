# A basic script for tagging specimen images with selected data as keywords, e.g. country, taxon name, etc, 
# as well as tags for copyright, license, etc.

# This script uses ExifTool.
# Make sure ExifTool is installed and available on your PATH first: https://exiftool.org/

# The dataset containing the keywords should have a field with the file names of the images you want to tag. See MakeImageRecords to generate this file.

# Note that you shouldn't have any fields with True and False values in your keywords dataset, as these 

#IMPORTS
import subprocess
import pandas as pd
import os 
from time import sleep, time, strftime, gmtime
from progress.bar import Bar

#SETTINGS

#collection details
collectionname = 'National Herbarium'
collectioncode = 'PRE'
collectiontype = 'vascular plants' #vertebrate fossils, reptiles, insects, etc

#fields from the dataset to tag images with
keywordfields = ['CONTINENT', 'COUNTRY', 'MAJORAREA', 'FAMILY', 'GENUS', 'SPECIES', 'COLLECTOR LASTNAME', 'ACCEPTEDGENUS', 'ACCEPTEDSPECIES']
typefield = 'HOMETSTAT' #using this will also add the keywork 'type' to the images if this field has a value
specimenurl = ''
fileNameField = 'filename'
specimenIdentifierField = "BARCODE" #the field that contains the identifier for the specimen in the image, e.g. catalogNumber
titleField = specimenIdentifierField #for the image title fields, should be specimenIdentifierField by default but can be used for other fields too
captionfield = "CAPTION" #for image captions/descriptions
sensitivefield = '' #a field indicating sensitive taxa

#copyrights, license, etc
copyright = "South African National Biodiversity Institute"
license = 'CC BY 4.0'
licenseurl = "https://creativecommons.org/licenses/by/4.0/"
rights = "Free to use for any purpose, including commercial purposes, with attribution. See License and AttributionName" #statement or URL
attribution = "South African National Biodiversity Institute"
attributionURL = "https://www.sanbi.org/"
creator = "Natural Science Collections Facility"

#filetype to target
fileext = '.tif'

#we might only want to tag some of the images so we can break the workload into manageable chunks
tagbatch = False #indicate whether to tag the batch or not
batchsize = 20000
startat = 900

#path and filename of dataset containing the specimen data
datafilepath = r'C:\general work\NSCF\TypeTagging' #keep this as a raw string so you don't have to escape the backslashes
datafile = r'PRE_Types-NonTypes_BODATSA_Aug_2022_combined_OpenRefine.csv'

#the directory with the images
image_dir = r'G:\PRE' #use if data in a different location to images, else...
#image_dir = datafilepath

#do you want to notify of any image files that were not found in the dataset?
writemissing = False
#writepath = r''
writepath = datafilepath
writefile = r'missingNonTypesAug2022_final.csv'

#only tag files included in a list - meant to be used with the output from 'writemissing' above.
#first column must be the file names, column name is ignored
#make sure that the file names in the list have file extensions (they may have been removed from writefile in order to extract from a database)
tagfromlist = False
#listpath = r''
listpath = datafilepath
listfile = r'missingNonTypesAug2022_final.csv'

#THE SCRIPT

start = time()
print()

#read the data file
print('reading data file...')
fullpath = os.path.join(datafilepath, datafile)
try: 
    df = pd.read_csv(fullpath)
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
    df = df.set_index(fileNameField, drop = False, verify_integrity = True)
except ValueError:
    print('There are duplicate values in the field \'', fileNameField + '\'')
    print('Please remove the duplicates and try again.')
    print('Quitting...')
    exit()

#check the file includes all the fields
allfields = [*keywordfields, specimenurl, typefield, specimenIdentifierField, titleField, captionfield, sensitivefield]
fieldsvals = [i for i in allfields if i is not None and i.strip() != '']

missingfields = []
for field in fieldsvals:
    if field not in df:
        missingfields.append(field)

if len(missingfields) > 0:
    print('The following fields are not in the dataset. Check spelling, case, and fix the dataset if needed:')
    print(' | '.join(missingfields))
    exit()

## read the directory of images, and slice if tagbatch == True
images = os.listdir(image_dir)
images = list(filter(lambda x: x.lower().endswith(fileext.lower()), images))

if len(images)  == 0:
    print('No images with file type', fileext, 'at', image_dir)
    print('Quitting...')
    exit()
else:
    if tagfromlist:
        print(len(images), 'images found in', image_dir)
    else:
        print(len(images), 'images found for tagging')

if tagbatch:
    images = images[startat:startat + batchsize]
    print(len(images), 'will be tagged in this batch')

#read the file list if requested
if tagfromlist:
    fullpath = os.path.join(listpath, listfile)

    try:
        filelist = pd.read_csv(fullpath)
    except Exception as e:
        print(e)
        print('Quitting...')
        exit()

    if filelist.empty: #no records in supplied file...
        print(f'No files listed in {listfile} --please check', listfile)
        print('Quitting...')
        exit()
    else:
        filelist = filelist.set_index(filelist.columns[0], drop = False)
        print(filelist.size, 'files to be tagged from', listfile)


#create the exiftool process
#For using subprocess see:
#see https://realpython.com/python-subprocess/
#see https://docs.python.org/3/library/subprocess.html
#see https://stackoverflow.com/a/22198788/3210158

#For running exiftool as a subprocess see -execute and -stay_open here:
#https://exiftool.org/exiftool_pod.html#Advanced-options
print('initializing exiftool...')
try:
    exiftool = subprocess.Popen(['exiftool', '-stay_open', 'True', '-@', '-', '-common_args', '-overwrite_original'], 
        stdin = subprocess.PIPE, 
        stdout = subprocess.PIPE)
except FileNotFoundError as e:
    print('ExifTool was not found on this system. Please make sure it is installed and available on the PATH')
    print('Bye bye...')
    exit()

print('  ', end = '') #this is needed for some reason...
print('\rStarting image tagging...', end='', flush=True)
blank = ' ' #for clearing printed values...

##loop through the images and add tags
count = 0
recordsnotfound = []
bar = Bar('Processing', max = len(images))
for image in images:

    if tagfromlist and not filelist.empty:
        if image not in filelist.index:
            bar.next()
            continue
    
    #the full file name and path
    imagepath = os.path.join(image_dir, image)

    #just for testing when we're trying to see if we reach the code below...
    #continue

    #get the keywords
    try:
        imagerecord = df.loc[image] #this searches using the index
    except:
        recordsnotfound.append(image)
        continue
    
    if imagerecord.empty: #I don't think this can happen, given the above...
        recordsnotfound.append(image)
        continue

    title = imagerecord[titleField]
    
    caption = ''
    if captionfield:
      caption = imagerecord[captionfield]

    keywords = []
    for field in keywordfields:
        keywords.append(imagerecord[field])

    #for types we want to add keyword 'type' if the type is not already 'type'
    if typefield:
        typeval = imagerecord[typefield]
        if typeval and str(typeval) != 'nan' and typeval.strip() != '':
            if typeval.lower() != 'type':
                keywords.append(typeval)            
            keywords.append('type') #all types are tagged as 'type'

    if sensitivefield:
        keywords.append(imagerecord[sensitivefield])

    if license:
        keywords.append(license)
    if collectiontype:
        keywords.append(collectiontype)
    if collectionname:
        keywords.append(collectionname)
    if collectioncode:
        keywords.append(collectioncode)

    #filter out nans/empty values and trim values
    keywords = [x for x in keywords if str(x) != 'nan' and x!= None and x.strip() != '']
    keywords = map(str.strip, keywords)

    #finally, get rid of any duplicate keywords...
    keywords = set(keywords)
    keywords = list(keywords)

    keywordsstring = ",".join(keywords)
    
    #tag the image
    exiftoolcmd = f'-title={title}{os.linesep} -xmp:description={caption}{os.linesep} -copyright={copyright}{os.linesep} -license={licenseurl}{os.linesep} -usageterms={rights}{os.linesep} -attributionname={attribution}{os.linesep} -attributionurl={attributionURL}{os.linesep} -creator={creator}{os.linesep} -xmp:subject={keywordsstring}{os.linesep} -sep{os.linesep} ,{os.linesep} {imagepath}{os.linesep} -execute{count}{os.linesep}'
    encodedcmd = exiftoolcmd.encode('utf-8')
    exiftool.stdin.write(encodedcmd)
    exiftool.stdin.flush()

    #now read the output from exiftool until we get to the end of the response message
    #we need this to keep the loop in sync with exiftool so we don't flood it
    output = ""
    newlines = 0
    while newlines < 2: 
        char = exiftool.stdout.read1(1)
        output += char.decode('utf-8')
        if os.linesep in output:
            newlines += 1
            output = ""
    
    exiftool.stdout.flush() #clear it so we can start on the next loop...

    count += 1
    bar.next()

#finish the exiftool process
print(f'\r{blank * 50}', end = '')
print('\rfinishing up.......', end = '')
endcmd = f'-stay_open{os.linesep}0{os.linesep}'
encmdencoded = endcmd.encode('utf-8')
exiftool.stdin.write(encmdencoded)
exiftool.stdin.flush()

#give it some time to close...
while exiftool.poll() == None:
    sleep(1)

end = time()
totaltime = strftime("%H:%M:%S", gmtime(end - start))
if count > 0:
    print(f'\r{count}', 'images tagged in', totaltime)
else:
    print('\rNo images were tagged...')

#print any images where records not found in the dataset
if len(recordsnotfound) > 0:
    print()

    if len(recordsnotfound) > 100:
        print('Records not found for', len(recordsnotfound), 'images')
    else:
        print('Could not find records for the following images:')
        print('|'.join(recordsnotfound))

    if writemissing:
        print()
        print('writing with missing records to file...')
        ofpath = os.path.join(writepath, writefile) #of = outfile
        newfile = not os.path.exists(ofpath)
        of = open(ofpath, 'a')
        oftext = '\r'.join(recordsnotfound)
        if newfile: # the file is created for the first time
            of.write('files\r')
        else:
            oftext = '\r' + oftext #we're appending so we need the first newline
        of.write(oftext)
        of.close()

#just feedback
print()
print('all done!')