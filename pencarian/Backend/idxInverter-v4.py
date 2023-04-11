"""
INVERTED INDEX MODULE
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 11:13:51 2022

@author: MVC
"""

import timeit
import pickle
import json
import sys

TERMS = []
RESFOLDER = 0
INVERTTIME = 0
# key = term, value = line counter
BUFFER = {}
# key = term, value = inverted idx, string
INVERTED = {}
# for checking purpose only
TERMSEXIST = set()

def importModel(vectorModel):
    global TERMS
    
    VECTORIZER = pickle.load(open(vectorModel, 'rb'))
    TERMS = VECTORIZER.get_feature_names()
    
    
def invertVec(vec, vecID):
    """
    Index inverter for vector.
    Get all vector input terms, append to inverted idx txt files as (vecID,weight)
    :param vec: vector dictionary (term:weight)
    :param vecID: string, vector ID (fileID-lineNo)
    :return: none
    """
    tic=timeit.default_timer()
    global TERMS
    global BUFFER
    global INVERTED
    global RESFOLDER
    global INVERTTIME
    global TERMSEXIST
    
    for term, value in vec.items():
        TERMSEXIST.add(term)
        # concate string inverted index (vecID, TFIDF)
        if term in INVERTED.keys():
            INVERTED[term] += vecID + ',' + str(value) + '\n'
            BUFFER[term] += 1
        else:
            INVERTED[term] = vecID + ',' + str(value) + '\n'
            BUFFER[term] = 1
            
        # check buffer to write
        if BUFFER[term] == 750:
            file = open(RESFOLDER + str(TERMS.index(term)) + '.txt', 'a')
            file.write(INVERTED[term])
            file.close()
            BUFFER[term] = 0
            INVERTED[term] = ''
        
    toc=timeit.default_timer()
    
    INVERTTIME = INVERTTIME + (toc - tic)
    
    # print (toc - tic)

def invertDocs(vecsFile, idFile):    
    """
    Read vector file per line, invert each vector using invertVec function
    :param vecsFile: String, vector file (txt file, 1 vector dict per line)
    :param idFile: String, vector IDs file (complete path)
    :return: none 
    """
    global INVERTED
    # get list of vector IDs
    file = open(idFile, 'r')
    ids = file.read().splitlines()
    file.close()

    # get vector dictionaries    
    idx = 0
    deleted = 0
    for dicti in open(vecsFile, 'r'):
        vec = json.loads(dicti.strip())
        if len(vec) < 10:
            invertVec(vec, ids[idx])
        else:
            deleted += 1
        idx = idx + 1
        if ((idx + 1) % 1000 == 0):
            # print("Current idx: " + str(idx))
            
    # print("Done " + str(idx) + " vecs")
    # print("Deleted " + str(deleted) + " vecs")
    
    # write inverted index for terms with less than 750 line
    for term, value in INVERTED.items():
        file = open(RESFOLDER + str(TERMS.index(term)) + '.txt', 'a')
        file.write(value)
        file.close()
        
def main(model, vecsFile, idFile, resFolder):
    """
    Main function
    :param model: String, path to vector model file (pickle)
    :param vecsFile: String, vector file (txt file, 1 vector dict per line)
    :param idFile: String, vector ID output files (complete path)
    :param resFolder: String, inverted index folder name (end with '/')
    :return: none
    """
    
    tic=timeit.default_timer()
    
    global RESFOLDER
    global INVERTTIME
    global TERMSEXIST
    
    RESFOLDER = resFolder
    importModel(model)
    invertDocs(vecsFile, idFile)
    toc=timeit.default_timer()
    
    total = toc - tic
    # print("Total terms: " + str(len(TERMSEXIST)))
    # print("Total time = " + str(total))
    # print("Inverting time = " + str(INVERTTIME))
    # print("Read time = " + str(total - INVERTTIME))
    
if __name__ == "__main__":
    model = str(sys.argv[1])
    vecsFile = str(sys.argv[2])
    idFile = str(sys.argv[3])
    resFolder = str(sys.argv[4])
    main(model, vecsFile, idFile, resFolder)