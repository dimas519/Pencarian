# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:22:11 2022

@author: MVC
"""

# Content format:
# Title, line number, line content (text), cosine score

import pandas as pd
import urllib.request
from urllib.request import Request, urlopen
from os import path



# UNCOMMENT KALAU MAU ONLINE
dir_path =path.dirname(path.realpath(__file__))
url = 'https://drive.google.com/file/d/1htZDKBIEpVYc9pdVHfr0Z032359Jdesn/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
CATALOG = pd.read_csv(url)

# UNCOMMENT KALAU MAU OFFLINE
# CATALOG = pd.read_csv(dir_path+"/CSV/targetBooks.csv")



#=================================================================================================================



# UNCOMMENT KALAU MAU ONLINE
url = 'https://drive.google.com/uc?id=' + 'https://drive.google.com/file/d/1b27OWnP-UcJwUn6VjzDYR7YaJUGrSfsi/view?usp=sharing'.split('/')[-2]
BOOK_LISTING = pd.read_csv(url)

#UNCOMMENT KALAU MAU OFFLINE
# BOOK_LISTING = pd.read_csv(dir_path+"/CSV/driveListing.csv")




def getTitle(fileNo):
    global CATALOG
    # print(CATALOG.head(2))
    # print('fileNo: ' + fileNo)

    result = CATALOG.loc[CATALOG['Text#'] == (fileNo)]['Title']
    # print("Result: " + result)
    if (result.empty):
        title = 0
    else:
        title = result.iloc[0]
        
    #print("Title " + title)
    return title

def getText(fileNo):
    global BOOK_LISTING
    
    # Catholic Theology too large to open directly from Drive
    if (fileNo == "CatholicTheologyLagrange"):
        # Change directory
        f = open(dir_path+"/invIdxSample2/CatholicTheology/(Catholic Theology) Reginald Garrigou-Lagrange - Reverend Reginald Garrigou-Lagrange Collec.txt", "r", encoding="utf8")
        text = f.read()
    else:
        result = BOOK_LISTING.loc[BOOK_LISTING['fileNo'] == (fileNo)]['reqURL']
        if (result.empty):
            text = 0
        else:
            url = result.iloc[0]
            with urllib.request.urlopen(url) as response:
                content = response.read()
            
            encoding = response.headers.get_content_charset('utf-8')
            text = content.decode(encoding)
    
    return text

def getLine(textList, lineNo):
    #print("Text Line: " + textList[int(lineNo)])
    return textList[int(lineNo)]