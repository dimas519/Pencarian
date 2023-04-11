# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:19:23 2023

@author: MVC
"""
from warnings import simplefilter 
simplefilter(action='ignore', category=DeprecationWarning)


import sys
import timeit
import pandas as pd


#Dibuat try catch biar gampang debugging
try:
    from Backend import searchByCosine as search
    from Backend import getContent
except :
    import searchByCosine as search
    import getContent






def main(query):
    search1=search.CosineSearch()
    
    
    
    invIdxFolder = 'invIdxSample2/'
    
    # UNCOMMENT KALAU MAU OFFLINE
    from os import path
    dir_path =path.dirname(path.realpath(__file__))
    vecModel = dir_path+'/MODELS/sampleModelTFIDF.pickle'
    tic=timeit.default_timer()
    search1.importModel(vecModel, invIdxFolder)
    
    # UNCOMMENT KALAU MAU ONLINE
    # url = "https://drive.google.com/uc?id=1GnXZAET0_pnNkcHIpVz4Ie_S2oHBG2iP"
    # tic=timeit.default_timer()
    # search1.importModel(url, invIdxFolder)
    
    
    
    
    search1.transformQuery(query)
    # print(search.QUERY) # gk usah
    
    search1.findAllCos()
    
    #result = search.findTopN(len(search.RELATED))
    
    result = search1.findTopN(20)
    
    # print dicti
    df = pd.DataFrame({'noFile':[], 'noParagraf':[], 'cosine':[], 'Judul':[], 'Teks':[]})
    currentFile = ''
    title = ''
    text = ''
    textList = []
    line = ''
    idx = 0
    

    
    for vecID, cosine in result.items():
        #if cosine < 0.4:
            #break
        vecID = vecID.split('-')
        fileNo = vecID[0]
        # print ('file: ' + fileNo, 'cosine: ',cosine) 
        lineNo = vecID[1]
        
        # check whether line comes from the same file as previous vecID
        # open new file if not
        if currentFile != fileNo:
            currentFile = fileNo
            
            
            title = getContent.getTitle(fileNo)
            text = getContent.getText(fileNo)
            if text != 0:
                textList = text.split('\n')
            else:
                textList = 0
        
        if textList != 0:
            line = getContent.getLine(textList, lineNo).rstrip()
            if (not line):
                line = '-'
        
  
        if (title != 0):
            
            # print({'fileID':str(fileNo) if fileNo != 'CatholicTheologyLagrange' else '10888', 'lineNo': str(lineNo), 'cosine': str(cosine), 'title': title, 'text': line})
            df = df.append({'noFile':str(fileNo) if fileNo != 'CatholicTheologyLagrange' else '10888', 'noParagraf': str(lineNo), 'cosine': str(cosine), 'Judul': title, 'Teks': line}, ignore_index=True)
            
            idx += 1
    
    
    
    toc=timeit.default_timer()
    
    
    total = toc - tic
    
    # print(df)
    # print(round(total,2))

    return df,round(total,2)
    
    
if __name__ == "__main__":

    
    query = str(sys.argv[1])
    main(query)