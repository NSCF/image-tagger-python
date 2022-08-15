import subprocess
import pandas as pd
import os 
from time import sleep, time, strftime, gmtime
import re

#This uses ExifTool: https://exiftool.org
#Make sure ExifTool is installed and available on your PATH first...

#SETTINGS

#fields to tag images with
collectionname = 'National Herbarium'
collectioncode = 'PRE'
collectiontype = 'vascular plants' #vertebrate fossils, reptiles, insects, etc

keywordfields = ['CONTINENT', 'COUNTRY', 'MAJORAREA', 'FAMILY', 'GENUS', 'SPECIES', 'COLLECTOR LASTNAME']
typefield = 'HOMETSTAT' #using this will also add the keywork 'type' to the images if this field has a value
specimenIdentifierField = "BARCODE" #the field that contains the identifier for the specimen in the image. Will be used for the title also
captionfield = "HOMETYPE"
sensitivefield = None

copyright = "South African National Biodiversity Institute"
license = 'CC BY 4.0'
licenseurl = "https://creativecommons.org/licenses/by/4.0/"
rights = "Free to use for any purpose, including commercial purposes, with attribution. See License and AttributionName" #statement or URL
attribution = "South African National Biodiversity Institute"
attributionURL = "https://www.sanbi.org/"

fileext = '.tif' #the file types to filter on, assumes all the same

##read csv as dataframe
csvpath = "C:\\temp\\Herbarium mass digitization project\\ImageTaggingExperiments"
csvfile = 'PRE_Types_BODATSA_July_2022-OpenRefine.csv'

#image_dir = "C:\temp\Herbarium mass digitization project\ImageTaggingExperiments"
image_dir = csvpath

#THE SCRIPT

start = time()
print()
print('Starting with image tagging...')

#read the data file
fullpath = os.path.join(csvpath, csvfile)
df = pd.read_csv(fullpath)
print(df.shape[0], 'records read from', csvfile)

#create the exiftool process
#For using subprocess see:
#see https://realpython.com/python-subprocess/
#see https://docs.python.org/3/library/subprocess.html
#see https://stackoverflow.com/a/22198788/3210158

#For running exiftool as a subprocess see -execute and -stay_open here:
#https://exiftool.org/exiftool_pod.html#Advanced-options
try:
    exiftool = subprocess.Popen(['exiftool', '-stay_open', 'True', '-@', '-', '-common_args', '-overwrite_original'], 
        stdin = subprocess.PIPE, 
        stdout = subprocess.PIPE)
except FileNotFoundError as e:
    print('ExifTool was not found on this system. Please make sure it is installed and available on the PATH')
    print('Bye bye...')
    exit()

##loop through the images and add tags
images = os.listdir(image_dir)
count = 0
recordsnotfound = []
for image in images:
    if (image.endswith)(fileext):

        #the full file name and path
        imagepath = os.path.join(image_dir, image)

        #get the keywords
        imagerecord = df.loc[df[specimenIdentifierField] == image.replace(fileext, '')]
        if imagerecord.empty:
            recordsnotfound.append(image)
            continue

        title = imagerecord[specimenIdentifierField].values[0]
        caption = imagerecord[captionfield].values[0]
        keywords = []
        for field in keywordfields:
            keywords.append(imagerecord[field].values[0])

        #for types we want to add keyword 'type' if the type is not already 'type'
        if typefield:
            typeval = imagerecord[typefield].values[0]
            if typeval and str(typeval) != 'nan' and typeval.strip() != '' and typeval.lower() != 'type':
                keywords.append('type')

        if sensitivefield:
            keywords.append(imagerecord[sensitivefield].values[0])

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

        keywordsstring = ",".join(keywords)
        
        #tag the image
        exiftoolcmd = f'-title={title}{os.linesep} -xmp:description={caption}{os.linesep} -copyright={copyright}{os.linesep} -license={licenseurl}{os.linesep} -usageterms={rights}{os.linesep} -attributionname={attribution}{os.linesep} -attributionurl={attributionURL}{os.linesep} -xmp:subject={keywordsstring}{os.linesep} -sep{os.linesep} ,{os.linesep} {imagepath}{os.linesep} -execute{count}{os.linesep}'
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
        if count % 5 == 0:
            print(count, 'images tagged',  end='\r', flush = True) #see https://stackoverflow.com/a/5419488/3210158


#finish the exiftool process
print('finishing up.......', end='\r')
endcmd = f'-stay_open{os.linesep}0{os.linesep}'
encmdencoded = endcmd.encode('utf-8')
exiftool.stdin.write(encmdencoded)
exiftool.stdin.flush()

#give it some time to close...
while exiftool.poll() == None:
    sleep(1)

end = time()
totaltime = strftime("%H:%M:%S", gmtime(end - start))
print(count, 'images tagged in', totaltime)

#print any images where records not found in the dataset
if len(recordsnotfound) > 0:
    print()
    print('Could not find records for the following images:')
    print('|'.join(recordsnotfound))

#just feedback
print()
print('all done!')