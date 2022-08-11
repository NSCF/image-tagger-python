import pandas as pd
import os 

#fields to tag images with
tagfields = ['CONTINENT', 'COUNTRY', 'MAJORAREA', 'FAMILY', 'GENUS', 'SPECIES', 'COLLECTOR LASTNAME',  'HOMETSTAT']
titlefield = "BARCODE"
captionfield = "HOMETYPE"
copyright = "South African National Biodiversity Institute"
license = 'CC BY 4.0'
licenseurl = "https://creativecommons.org/licenses/by/4.0/"
rights = "Free to use for any purpose, including commercial purposes, with attribution. See License and AttributionName"
attribution = "South African National Biodiversity Institute"
attributionURL = "https://www.sanbi.org/"

#TODO add sensitive column

fileext = '.tif'

##read csv as dataframe
csvpath = "C:\\temp\\Herbarium mass digitization project\\ImageTaggingExperiments"
csvfile = 'PRE_Types_BODATSA_July_2022-OpenRefine.csv'

#image_dir = "C:\temp\Herbarium mass digitization project\ImageTaggingExperiments"
image_dir = csvpath

#THE SCRIPT

fullpath = os.path.join(csvpath, csvfile)
df = pd.read_csv(fullpath)
print(df.shape[0], 'records read from', csvfile)

##read in images from directory
images = os.listdir(image_dir)
count = 0
#tag multiple images with unique keywords
recordsnotfound = []
for image in images:
    if (image.endswith)(fileext):

        #get the exif data
        imagepath = os.path.join(image_dir, image)
        #exif_dict = piexif.load(imagepath)

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

        keywords.append(license)
 
        #filter out nans/empty values
        keywords = [x for x in keywords if str(x) != 'nan' and x != None]
        #tag the image
        keywordsstring = ",".join(keywords)

        exiftoolcmd = f'exiftool -title="{title}" -caption="{caption}" -copyright="{copyright}" -license="{licenseurl}" -usageterms="{rights}" -attributionname="{attribution}" -attributionurl="{attributionURL}" -xmp:subject="{keywordsstring}" -sep ","  -overwrite_original "{imagepath}"'
        os.system(exiftoolcmd)
        
        #show progress
        count += 1
        if(count % 10 == 0):
            print(count, 'images tagged')

if len(recordsnotfound) > 0:
    print()
    print('Could not find records for the following images:')
    print('|'.join(recordsnotfound))

#just feedback
print()
print('all done')