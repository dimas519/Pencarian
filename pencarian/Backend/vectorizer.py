"""
TEXT VECTORIZER MODULE
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 14:21:53 2022

@author: MVC
"""
import re
import gc
import sys
import json
import math
import pickle
from os import walk
from os import path
from scipy.sparse import find


try:
    from Backend import preprocessing as pr
except:
    import preprocessing as pr

class Vectorizer():
    def __init__(self): 
        self.vectorizer=0
        self.terms=0
        # VECTORIZER = 0
        # TERMS = 0

    def loadData(filename, preprocess):
        """
        Read txt file
        :param filename: string
        :param preprocess: int
            # 0 - no lemma
            # 1 - simple lemma
            # 2 - best lemma (Spacy)
        :return list of text
        """
        file = open(filename, 'r', encoding="utf8")
        Lines = file.readlines()
        
        # 1 doc / line
        if int(preprocess) == 2:
            for idx,line in enumerate(Lines):
                Lines[idx] = pr.lemmaSpacy(line.strip())
                # print('lemmatized line ' + str(idx))
        elif int(preprocess) == 0:
            for idx,line in enumerate(Lines):
                Lines[idx] = line.strip()
                
        return Lines

    def loadVectorizer(self,vectorModel):
        """
        Set global variable VECTORIZER & TERMS
        :param vectorModel: string, vector model file
        :return none
        """
        self.vectorizer = pickle.load(open(vectorModel, 'rb'))
        self.terms = self.vectorizer.get_feature_names()

    def vectorizerTFIDF(self,txt):
        """
        Vectorize text input, weight: TF IDF
        :param txt: string
        :return vector as dictionary
        """
        
        dicti = {}

        df = []
        # open vectorizer model
        
        df.append(txt)

        # vectorize
        X_matrix = find(self.vectorizer.transform(df))

        # non zero term indices
        X_idx = X_matrix[1]
        # non zero term weight
        tfidf = X_matrix[2]
        
        # build term:idf dictionary
        for cnt, idx in enumerate(X_idx):
            dicti[self.terms[idx]] = tfidf[cnt]

        # print("dicti",dicti)
        return dicti

    def vectorizerCount(self,txt):
        """
        Vectorize text input, weight: count
        :param txt: string
        :return vector as dictionary
        """


        
        dicti = {}

        df = []
        # open vectorizer model
        
        df.append(txt)

        # vectorize
        X_matrix = find(self.vectorizer.transform(df))
        ## print('\nTransform result')
        ## print(X_matrix)
        
        # non zero term indices
        X_idx = X_matrix[1]
        # non zero term weight
        count = X_matrix[2]

        # build term:count dictionary
        for cnt, idx in enumerate(X_idx):
            dicti[self.terms[idx]] = int(count[cnt])
            
        ## print(dicti)

        return dicti

    def vecL2(self, vec):
        """
        Calculate vector L2 norm
        :param vec: dictionary (term:weight)
        :return float
        """
        length = 0
        for value in vec.values():
            length += (float(value) * float(value))
            
        length = math.sqrt(length)
        return length

    def normalizer(self,vec, l2):
        """
        Normalize vector using L2 norm
        :param vec: dictionary (term:weight)
        :param l2: float, l2 norm
        :return vector as dictionary
        """
        dicti = {}
        
        for term, value in vec.items():
            dicti[term] = value / l2
        
        return dicti

    def main(fn, model, vectorFile, idFile):
        """
        Main function
        :param fn: String, path to folder input (end with '/')
        :param model: String, path to vector model file (pickle)
        :param vectorFile: String, vector dictionary output file name (complete path)
        :param idFile: String, vector ID output file name (complete path)
        :return: none
        """
        
        # get all files' name in folder
        fileNames = next(walk(fn), (None, None, []))[2]
        
        # get all text from all files in input folder
        df = [] # list of text
        lines = [] # list of lines
        fileID = [] # list of dictionary (file name : num of line), used for ID generator
        tempID = ''
        lineNum = 0
        
        for fileName in fileNames:
            # get file name without txt, for vector ID
            tempID = re.sub('\.txt$', '', fileName)
            # get file full path
            fileName = fn + fileName
            # print(fileName)
            # load data
            txt = loadData(fileName, 0)
            # save num of line
            lineNum = len(txt)
            lines.append(lineNum)
            # create info for ID generator (fileID : numOfLine)
            fileID.append({tempID:int(lineNum)})
            # dataframe
            df = df + txt
        
        # save file name and num of lines per file
        #pickle.dump(fileNames, open('../DATA/FileList/part1FileNames.pickle', 'wb'))
        #pickle.dump(lines, open('../DATA/FileList/part1LineNums.pickle', 'wb'))
        
        # print ("Load data: DONE, " + str(len(df)) + ' lines')
        del tempID
        del lineNum
        gc.collect()
        
        # load vector model
        loadVectorizer(model)
        # print ("Load vector: DONE")
        

        outputVector = open(vectorFile, "w")
        outputID = open(idFile, "w")
        
        # line number, start from 0 for new file
        count = 0
        # trace fileID array to get num of line
        cursor = 0
        # current File number
        currFile = list(fileID[cursor].keys())[0]
        lineNum = list(fileID[cursor].values())[0]
        
        for idx,txt in enumerate(df):
            # create vector ID
            if count >= (lineNum):
                count = 0
                cursor += 1
                currFile = list(fileID[cursor].keys())[0]
                lineNum = list(fileID[cursor].values())[0]
                
            # ID: fileID-LineNo
            tempID = str(currFile) + '-' + str(count)
            count += 1
            
            # write ID in txt file
            # vecID: fileNo-lineNo
            outputID.write(tempID + '\n')
            
            # TFIDF vectorizer
            tempDict = vectorizerTFIDF(txt)
            
            # line marker
            ## print ("line " + str(idx))
            ## print (tempDict)
            
            # write to output vector in txt file
            # 1 dictionary (term:value) per line
            outputVector.write(str(json.dumps(tempDict))+'\n')
            
            # gCollector
            del tempDict
            del txt
            del tempID
            if idx % 5000 == 0:
                gc.collect()
            #listOfDict.append(tempDict)
            
        gc.collect()
        
        # print ("Create dictionary: DONE")
        outputVector.close()
        outputID.close()
        
    # =============================================================================
    # FOR TRIAL PURPOSE
    # def main():
    #     # print("Input folder")
    #     fn = input()
    #     # get all files' name in folder
    #     fileNames = next(walk(fn), (None, None, []))[2]
    #     
    #     i = 0
    #     count = 0
    #     while count < 34229:
    #         fileName = fn + fileNames[i]
    #         # print(fileName)
    #         txt = loadData(fileName)
    #         count = count + len(txt)
    #         i = i + 1
    # =============================================================================
        
    if __name__ == "__main__":
        fn = str(sys.argv[1])
        model = str(sys.argv[2])
        vectorFile = str(sys.argv[3])
        idFile = str(sys.argv[4])
        main(fn, model, vectorFile, idFile)