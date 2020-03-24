
from flask import Flask
from flask import Flask, jsonify
import spacy
from flask import request

#%matplotlib inline
#import matplotlib.pyplot as plt
#plt.rcParams['font.size'] = 14
from spacy.lang.en import English


nlp = English()
#import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
from spacy.matcher import PhraseMatcher
import requests
import codecs
import urllib.request, json 
from pandas.io.json import json_normalize


#function that does phrase matching and builds a candidate profile
def create_profile(textDat):
    #text = pdfextract(file) 
    textDat = str(textDat)
    textDat = textDat.replace("\\n", "")
    textDat = textDat.lower()
    #below is the csv where we have all the keywords, you can customize your own
  #  T=tc
  #  T=T.lower()
   # dfObj = pd.DataFrame()
  #  dfObj = dfObj.append({'tText': T}, ignore_index=True)
  #  NLR_words = [nlp(text) for text in dfObj['tText'].dropna(axis = 0)]
    #x = [element.lower() for element in tc]
    #NLR_words = [nlp(text) for text in x]
    
    r = requests.get('https://maftalentsearchstorage.blob.core.windows.net/mafresumerepo/skillsets/Skills.json?st=2020-03-15T12%3A29%3A28Z&se=2020-03-31T12%3A29%3A00Z&sp=rl&sv=2018-03-28&sr=b&sig=rUKnQsR82ALuRQUMZmlrpHYVdej5ApyAag4M6gUE%2BUU%3D')
    #print (r.json())

    #decoded_data=codecs.decode(r.text.encode(), 'utf-8-sig')
    #data = json.loads(decoded_data.lower())
    
    decoded_data=codecs.decode(r.text.encode(), 'utf-8-sig')
    data = json.loads(decoded_data.lower())

    df=json_normalize(data)
    words = [nlp(text) for text in df['name'].dropna(axis = 0)]

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Data', None, *words)
    
    
    

    doc = nlp(textDat)

    d = []  
    matches = matcher(doc)
    #print(matches,'rrrrrrrrrrrrrrrrrr')
    for match_id, start, end in matches:
       # print(match_id,',,,,,,,,,,,,,,,,,')
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())



    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))

    #base = os.path.basename(file)
    #filename = os.path.splitext(base)[0]

    #name = filename.split('_')
 #   name2 = name[0]
  #  name2 = name2.lower()
    ## converting str to dataframe
  #  name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])

  #  dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
  #  dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
    return(df3)

def create_profileResr(text):
    #text = pdfextract(file) 
    text = str(text)
    return((text))


app = Flask(__name__)

app.debug = True

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/jsonResr', methods=['POST']) 
def textFormatOld():
    req_data = request.get_json()
    language = req_data['textDat']
    v=str(language)
    return (v)

@app.route('/json', methods=['POST']) 
def textFormat():
    req_data = request.get_json()
    language = req_data['textDat']
    r=create_profile(language)
    r=r.loc[r['Count'] > '1']
    return (r.to_json(orient='records'))




