#Find images in a directory that have not been tagged with keywords...

#IMPORTS
import subprocess
import pandas as pd
import os 
from time import sleep, time, strftime, gmtime

#SETTINGS

#the directory with the images
image_dir = r'G:\PRE' #use if data in a different location to images, else...

#filetype to target
fileext = '.tif'

#the file to write results to
writefile = r'imagesNotFound.csv'

#SCRIPT

start = time()
print()

try:
    exiftool = subprocess.Popen(['exiftool', '-stay_open', 'True', '-@', '-'], 
        stdin = subprocess.PIPE, 
        stdout = subprocess.PIPE)
except FileNotFoundError as e:
    print('ExifTool was not found on this system. Please make sure it is installed and available on the PATH')
    print('Bye bye...')
    exit()

print('  ', end = '') #this is needed for some reason...
print('\rStarting to read images...', end='')

## read the directory of images
images = os.listdir(image_dir)

##loop through the images and add tags
count = 0
nottagged = []
for image in images:
    if (image.endswith)(fileext):

        keywords = ''

        #the full file name and path
        imagepath = os.path.join(image_dir, image)
 
        
        #read the keywords tag
        exiftoolcmd = f'-subject{os.linesep} {imagepath}{os.linesep} -execute{os.linesep}'
        encodedcmd = exiftoolcmd.encode('utf-8')
        exiftool.stdin.write(encodedcmd)
        exiftool.stdin.flush()

        #now read the output from exiftool until we get to the end of the response message
        #we need this to keep the loop in sync with exiftool so we don't flood it
        output = ""
        ready = False
        next = False
        while not ready: 
            char = exiftool.stdout.read1(1)
            try:
              output += char.decode('utf-8')
            except:
              nottagged.append(image) #we assume there is a problem and tags must be written again
              next = True
              break
              
            if f'{{ready}}{os.linesep}' in output:
              ready = True
        
        if(next): 
          continue
        
        exiftool.stdout.flush() #clear it so we can start on the next loop...

        if 'Subject' in output: #here we check if it's blank
          keywords = output.split(os.linesep)[0].split(':')[1].strip().split(',')
          keywords = map(str.strip, keywords)
          #filter out nans/empty values and trim values
          keywords = [x for x in keywords if str(x) != 'nan' and x!= None and x != '']
          if len(keywords) == 0: #
            nottagged.append(image)
        else: #here it doesn't exist at all
          nottagged.append(image)
      

        count += 1
        if count % 5 == 0:
            print('\r', count, 'images checked...', end ='',  flush = True) #see https://stackoverflow.com/a/5419488/3210158, moved carriage return to the start

#finish the exiftool process
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
print('\r', count, 'images checked in', totaltime)


if len(nottagged) > 0 :
  print(len(nottagged), 'do not have keywords, see', writefile)
  ofpath = os.path.join(image_dir, writefile) #of = outfile
  of = open(ofpath, 'w')
  of.write('file\r')
  oftext = '\r'.join(nottagged)
  of.write(oftext)
  of.close()
else:
  print('all images have keywords')

print('All done...')

