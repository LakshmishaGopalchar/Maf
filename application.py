
from flask import Flask
from flask import Flask, jsonify
import spacy


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


#function that does phrase matching and builds a candidate profile
def create_profile(text,tc):
    #text = pdfextract(file) 
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()
    #below is the csv where we have all the keywords, you can customize your own
    T=tc
    T=T.lower()
    dfObj = pd.DataFrame()
    dfObj = dfObj.append({'tText': T}, ignore_index=True)
    NLR_words = [nlp(text) for text in dfObj['tText'].dropna(axis = 0)]
    


    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Data', None, *NLR_words)
    
    
    

    doc = nlp(text)

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


app = Flask(__name__)

app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/json', methods=['POST']) 
def textFormat():
    req_data = request.get_json()
    
    language = req_data['textDat']
    framework = req_data['keyData']
    
   # text = request.args.get('text')
    #print(language)
   # key = request.args.get('key')
    #print(framework)
    r=create_profile(language,framework)
    return (r.to_json(orient='index'))




