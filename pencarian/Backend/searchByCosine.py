"""
SEARCH MODULE
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:12:18 2022

@author: MVC
"""

import sys
import timeit
import itertools
from os import path


try:
    from Backend import vectorizer
except:
    import vectorizer


class CosineSearch:
    def __init__(self):
        self.query = 0
        # inverted index folder path
        self.invidx = 0
        # cosine value for every related doc (key:vecID, value:cosine)
        self.related = {}
        # l2 norm file name
        #L2FILE = ''
        self.vectorizer1=vectorizer.Vectorizer()


    def importModel(self,vectorModel, invIdxFolder):
    
        
        self.vectorizer1.loadVectorizer(vectorModel)
        self.invidx = invIdxFolder
        
    def transformQuery(self,query):
        '''
        Transform query to normalized vector
        :param query: String
        :return none
        '''

        
        self.query = self.vectorizer1.vectorizerTFIDF(query)
        #QUERY = vectorizer.normalizer(QUERY, vectorizer.vecL2(QUERY))
        

    def findAllCos(self):
        '''
        Find all related vector
        :return none
        '''
        

        
        # for each related vector Vi, calculate dot product between query and Vi
        # related vector: vector with at least 1 similar term from query
        for term, value in self.query.items():
            dir_path =path.dirname(path.realpath(__file__))
            
            file = open(dir_path+"/"+self.invidx + str(self.vectorizer1.terms.index(term))+'.txt', 'r', encoding="utf8")     
            
            # related set (vecIDs, weight value)
            vecSets = file.read().split('\n')
            file.close()
            # print(term + ' - ' + str(vectorizer.TERMS.index(term)))
            for vecSet in vecSets[:-1]:
                # vecSet format: vecID,weight
                # vecList: [vecID, weight]
                vecList = vecSet.split(',')
                if vecList[0] in self.related.keys():
                    self.related[vecList[0]] += value * float(vecList[1])
                else:
                    self.related[vecList[0]] = value * float(vecList[1])
                    
    # =============================================================================
    #     # FOR UNNORMALIZED VECTOR
    #     # for each related vector Vi, calculate cosine similarity between query and Vi
    #     l2norms = open(L2FILE, 'r')
    #     for vecID, dotProd in RELATED.items():
    #         l2norm = 1
    #         for line in l2norms:
    #             # line format: vecID,l2norm
    #             if vecID in line:
    #                 l2norm = float(line.split(',')[1])
    #                 break
    #         RELATED[vecID] = dotProd / l2norm
    # =============================================================================
            
    def findTopN(self,n):
        '''
        Find top n related vector
        :return dictionary, top n related vector (vecID:cosine)
        '''
        
        sortRelated = dict(sorted(self.related.items(), key=lambda item:item[1], reverse=True))
        return dict(itertools.islice(sortRelated.items(), n))


    # def main(vecModel, invIdxFolder, l2File, query, n = 5):
    # use header above for unnormalized vectors
    def main(vecModel, invIdxFolder, query, n = 20):
        """
        Main function
        :param vecModel: String, path to vector model file (pickle)
        :param invIdxFolder: String, inverted index folder (end with '/')
        :param l2File: String, l2 norms file name (complete path)
        :param query: String, query
        :param n: int, number of related doc (default: 20)
        :return: none
        """
        
        #global L2FILE
        #L2FILE = l2File
        
        tic=timeit.default_timer()
        importModel(vecModel, invIdxFolder)
        
        transformQuery(query)
        # print(QUERY)
        
        findAllCos()
        
        result = findTopN(n)
        
        # print dicti
        # for vecID, cosine in result.items():

            # print(vecID + ': ' + str(cosine))
        
        toc=timeit.default_timer()
        
        total = toc - tic
        # print("Total time = " + str(total))
        
    if __name__ == "__main__":
        model = str(sys.argv[1])
        invIdxFolder = str(sys.argv[2])
        #l2File = str(sys.argv[3])
        query = str(sys.argv[3])
        
        if len(sys.argv) > 4:
            n = int(sys.argv[4])
            main(model, invIdxFolder, query, n)
            #main(model, invIdxFolder, l2File, query, n)
        else:
            main(model, invIdxFolder, query)
            #main(model, invIdxFolder, l2File, query)