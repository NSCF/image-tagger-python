import pandas as pd
import os 

#This uses ExifTool: https://exiftool.org
#Make sure ExifTool is installed and available on your PATH first...

#SETTINGS

#fields to tag images with
collectionname = 'National Herbarium'
collectioncode = 'PRE'
collectiontype = 'vascular plants' #vertebrate fossils, reptiles, insects, etc

tagfields = ['CONTINENT', 'COUNTRY', 'MAJORAREA', 'FAMILY', 'GENUS', 'SPECIES', 'COLLECTOR LASTNAME']
typefield = 'HOMETSTAT' #using this will also add the keywork 'type' to the images if this field has a value
titlefield = "BARCODE"
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

#read the data file
fullpath = os.path.join(csvpath, csvfile)
df = pd.read_csv(fullpath)
print(df.shape[0], 'records read from', csvfile)

##loop through the images and add tags
images = os.listdir(image_dir)
count = 0
recordsnotfound = []
for image in images:
    if (image.endswith)(fileext):

        #get the exif data
        imagepath = os.path.join(image_dir, image)

        #get the keywords
        imagerecord = df.loc[df['BARCODE'] == image.replace(fileext, '')]
        if imagerecord.empty:
            recordsnotfound.append(image)
            continue

        title = imagerecord[titlefield].values[0]
        caption = imagerecord[captionfield].values[0]
        keywords = []
        for field in tagfields:
            keywords.append(imagerecord[field].values[0])

        #for types we want to add keyword 'type' if the type is not already 'type'
        if typefield:
            typeval = imagerecord[typefield].values[0]
            if typeval and str(typeval) != 'nan' and typeval.strip() != '' and typeval.lower() != 'type':
                keywords.append('type')

        if sensitivefield:
            keywords.append(imagerecord[sensitivefield].values[0])

        keywords.append(license)
        keywords.append(collectiontype)
        keywords.append(collectionname)
        keywords.append(collectiontype)
 
        #filter out nans/empty values and trim values
        keywords = [x for x in keywords if str(x) != 'nan' and x!= None and x.strip() != '']
        keywords = map(str.strip, keywords)

        keywordsstring = ",".join(keywords)
        
        #tag the image
        exiftoolcmd = f'exiftool -title="{title}" -xmp:description="{caption}" -copyright="{copyright}" -license="{licenseurl}" -usageterms="{rights}" -attributionname="{attribution}" -attributionurl="{attributionURL}" -xmp:subject="{keywordsstring}" -sep ","  -overwrite_original "{imagepath}"'
        os.system(exiftoolcmd)
        
        #show progress
        count += 1
        if(count % 10 == 0):
            print(count, 'images tagged')

#print any images where records not found in the dataset
if len(recordsnotfound) > 0:
    print()
    print('Could not find records for the following images:')
    print('|'.join(recordsnotfound))

#just feedback
print()
print('all done')