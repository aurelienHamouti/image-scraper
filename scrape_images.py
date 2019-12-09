#environnement : python3 with libraries here
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse
import time
import random

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

def scrape_images_by_page(subject, header, resultIndex, directory):
    subject = subject.split()
    subject='+'.join(subject)
    url="http://www.bing.com/images/search?q=" + subject + "&FORM=HDRSC2&selectedindex=" + resultIndex 
    soup = get_soup(url,header)
    pageImages=[]# contains the link for Large original images, type of image
    for a in soup.find_all("a",{"class":"iusc"}):
        m = json.loads(a['m'])
        turl = m["turl"]
        murl = m["murl"]
        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        print('image loaded : '  + image_name)
        pageImages.append((image_name, turl, murl))
    print("there are total" , len(pageImages),"images loaded")

    if not os.path.exists(directory):
        os.mkdir(directory)
    fullDirectory = os.path.join(directory, subject.split()[0])
    if not os.path.exists(fullDirectory):
        os.mkdir(fullDirectory)

    print('images recording in the directory ' + fullDirectory + ' in process')
    for i, (image_name, turl, murl) in enumerate(pageImages):
        try:
            raw_image = urllib.request.urlopen(turl).read()
            Imagefile = Path(os.path.join(fullDirectory, image_name))
            if Imagefile.is_file():#check if the image already exists in the directory to avoid a duplicate
                print('file ' + Imagefile.name + ' already exists')
            else:
                f = open(os.path.join(fullDirectory, image_name), 'wb')
                f.write(raw_image)
                print('image ' + image_name + ' is recorded in directory ' + fullDirectory)
                f.close()
        except Exception as e:
            print("could not load : " + image_name)
            print(e)

#---main programm---
directoryTarget="pets" 
browserHeader={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
indexMax = 500 #~ nb max images we want, warning !!! bing is limited for number of images by research
lstSubjects = ['kitten','puppy','bird','dog','cute+animal','poney'] #target subject 

for subject in lstSubjects:
    i = 0 #init
    while i < indexMax: 
        time.sleep(random.random()) #random sleep to evoid to be blacklist by search engine
        scrape_images_by_page(subject, browserHeader, str(i), directoryTarget)
        i += 30 #increment by 30 because it's ~ nb imgages by bing page result
print('END of the programme')
sys.exit(0)
