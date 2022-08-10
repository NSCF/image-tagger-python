import piexif
import pandas as pd
import os 
from os import listdir
from math import nan, isnan

#fields to tag images with
tagfields = ['COUNTRY', 'FAMILY', 'HOMETSTAT', 'TYPEOF', 'MAJORAREA']

##read csv as dataframe
csvpath = "C:\\temp\\Herbarium mass digitization project\\ImageTaggingExperiments"
csvfile = 'PRE_Types_BODATSA_July_2022-OpenRefine.csv'
fullpath = os.path.join(csvpath, csvfile)
df = pd.read_csv(fullpath)
print(df.shape[0], 'records read from', csvfile)


#image_dir = "C:\temp\Herbarium mass digitization project\ImageTaggingExperiments"
image_dir = csvpath


##read in images from directory
images = os.listdir(image_dir)
count = 0
#tag multiple images with unique keywords
for image in images:
    if (image.endswith)(".jpg"):

        #get the exif data
        imagepath = os.path.join(image_dir, image)
        exif_dict = piexif.load(imagepath)

        #get the keywords
        imagerecord = df.loc[df['BARCODE'] == image.replace('.jpg', '')]
        keywords = []
        for field in tagfields:
            keywords.append(imagerecord[field].values[0])
 
        #filter out nans
        keywords = [x for x in keywords if str(x) != 'nan' and x != None]
        #tag the image
        keywordsstring = "; ".join(keywords)
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywordsstring.encode("utf-16le") 
        new_exif = piexif.dump(exif_dict)
        piexif.insert(new_exif, imagepath)
        
        #print 
        count += 1
        if(count % 10 == 0):
            print(count, 'images tagged')

print('all done')