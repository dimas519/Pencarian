from os import path
import json
import re 
import random 
import string
import time

def save(jsonInput):
    saveDir=path.dirname(path.realpath(__file__))+"/unpulledJson/"
    
    
    
    json_object = json.loads(jsonInput) 
    json_object_dump=json.dumps(json_object, indent = 2) 

    title=json_object['query']
    title = re.sub('[^A-Za-z0-9\' ]', '', str(title))
    
    success=False;
    numberRetry=0;
    
    named_tuple = time.localtime() 
    time_string = time.strftime("%Y:%m:%d:%H:%M:%S", named_tuple)
    
    
    
    while not success:
        
        identifier=''.join(random.choices(string.ascii_letters+ string.digits,k=10)) 
        
        
        saveFileName="{}{}-{}-{}.json".format(saveDir,time_string,title,identifier)
        
        
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
        
    
    
    
    
    
    
    
    

    
    



jsonInput='''
    {
   "query": "adam smith",
   "result": [
      {
         "noFile": "10888",
         "noParagraf": "15863",
         "relevan": true
      },
      {
         "noFile": "10888",
         "noParagraf": "16056",
         "relevan": true
      },
      {
         "noFile": "10888",
         "noParagraf": "16249",
         "relevan": true
      },
      {
         "noFile": "10888",
         "noParagraf": "16442",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "16635",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "16828",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "17021",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "17214",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "17407",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "17600",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "17793",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "17986",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "18179",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "18372",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "18565",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "18758",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "18951",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "19144",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "19337",
         "relevan": false
      },
      {
         "noFile": "10888",
         "noParagraf": "19530",
         "relevan": false
      }
   ]
}
    '''
    
    
y=save(jsonInput)
print(y)