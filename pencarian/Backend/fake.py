import random
import pandas as pd






def createDataFrame(query,loop=0):
    data=[]
    for i in range(0,20,1):
        doc=[]
        doc.append(random.randint(1,10)) 
        doc.append(random.randint(1,150))
        doc.append("LOREM IPSUM {}".format(i+1))
        doc.append("{} Lorem Ipsum {} is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.".format(query,(i+1)))

        data.append(doc)
    for p in range(0,loop,1): #spare waktu  buat proses backend
        v=0

        
    df=pd.DataFrame(data,columns=['noFile','noParagraf','Judul','Teks'])
    return df

