# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:27:41 2022

@author: MVC
"""

import sys
import timeit
import searchByCosine as search
import getContent

def main(query):
    vecModel = 'Models/sampleModelTFIDF.pickle'
    invIdxFolder = 'invIdxSample2/'
    
    tic=timeit.default_timer()
    search.importModel(vecModel, invIdxFolder)
    
    search.transformQuery(query)
    print(search.QUERY)
    
    search.findAllCos()
    
    #result = search.findTopN(len(search.RELATED))
    
    result = search.findTopN(20)
    
    # print dicti
    resFile = open('C:/GUTENBERG/expResult/' + query + '.csv', 'w')
    resFile.write('fileNo,lineNo,cosine,title,text\n')
    currentFile = ''
    title = ''
    text = ''
    textList = []
    line = ''
    
    for vecID, cosine in result.items():
        #if cosine < 0.4:
            #break
        vecID = vecID.split('-')
        fileNo = vecID[0]
        print ('file: ' + fileNo)
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
            line = getContent.getLine(textList, lineNo)
            if (not line):
                line = '-'
        
        if (title != 0):
            resFile.write(fileNo + ',' + lineNo + ',' + str(cosine) + ',"' + title + '","' + line + '"\n')
    
    resFile.close()
    
    toc=timeit.default_timer()
    
    total = toc - tic
    print("Total time = " + str(total))
    
if __name__ == "__main__":
    query = str(sys.argv[1])
    main(query)