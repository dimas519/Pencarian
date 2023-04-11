from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader



#untuk backend 
import json
from Backend import engine



from Backend import fake
import logging
from jsonSaved import saveJson


    

def index(request):
    logger = logging.getLogger(__name__)
    
    query=request.GET.get('query', '')
    if(not query==''):
        logger.info("query"+get_client_ip(request))
        return data(query)
    else:
        df=fake.createDataFrame("test")
        
        context ={
        "df":df
        }
        
        
        
           
        template = render(request,"production.html",context)
        logger.info("view prod"+get_client_ip(request))
        return template
    
def data(query):
    
        
    # df=fake.createDataFrame(query,0)
    result=engine.main(query)
    df=result[0]
    #800000000
    data=df.to_dict(orient='records')
    
    result={
        "time":result[1],
        "data":data
    }
        

    return HttpResponse(json.dumps(result), content_type="application/json")



def experimentView(request):
    get_client_ip(request)
    df=fake.createDataFrame("test")
        
    context ={
    "df":df
    }
    
    template = render(request,"experiment.html",context)
    
    
    logger = logging.getLogger(__name__)
    logger.info("view expr"+get_client_ip(request))
    return template



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
    else:
       ip = request.META.get('REMOTE_ADDR')
       print(ip)
    return ip


def save(request):
    
    logger = logging.getLogger(__name__)
    logger.info("save"+get_client_ip(request))
    
    result={}
    query=request.GET.get('save', '')
    if(not query==''):
        result['result']=saveJson.save(query)
    else:
        result['result']=False

    return HttpResponse(json.dumps(result), content_type="application/json")
