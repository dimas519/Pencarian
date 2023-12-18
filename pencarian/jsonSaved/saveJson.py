from os import path
import json
import re 
import random 
import string
import time

def save(jsonInput):
    saveDir=path.dirname(path.realpath(__file__))+"/unpulledJson/"
    print(saveDir)
    
    
    json_object = json.loads(jsonInput) 
    json_object_dump=json.dumps(json_object, indent = 2) 

    title=json_object['query']
    title = re.sub('[^A-Za-z0-9\' ]', '', str(title))
    
    success=False;
    numberRetry=0;
    
    named_tuple = time.localtime() 
    time_string = time.strftime("%Y-%m-%dT%H_%M_%S", named_tuple)
    
    
    
    while not success:
        
        identifier=''.join(random.choices(string.ascii_letters+ string.digits,k=10)) 
        
        
        saveFileName="{}{}-{}-{}.txt".format(saveDir,time_string,title,identifier)
        
        
        try:
            saveFile=open(saveFileName,"x")
            
            saveFile.write(json_object_dump)
            saveFile.close()
            success=True
            return True
        except BaseException as e:
            print(str(e))
            success=False
            numberRetry+=1
            
            if(numberRetry==5):
                return False;

