import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
import os
from dotenv import load_dotenv 
import subprocess
from db import get_connection
load_dotenv()

import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from nltk.stem import WordNetLemmatizer
from stop_words import get_stop_words
import nltk
import string
nltk.download('wordnet')
nltk.download('omw-1.4')

use_sql = os.getenv("use_sql")
use_sql = use_sql == 'True'

if use_sql:
    engine = get_connection()
    conn = engine.connect()
    
def preprocessing(text):
  '''
  This function takes raw text Converts uppercase to Lower, Removes special charecters, stop words 
  and text that follows special charecters (Ex \xe3\x80\x80\)
  '''

  text=text.strip() #Strips the sentence into words
  text = text.lower() #Converts uppercase letters to lowercase
  text = text.split(' ') #Splitting sentence to words
  dummy = []
  for i in text:
    if i[:2] == '\\x':
      special_texts = [i.split("\\") for i in text if i[:2] == '\\x']
      for j in special_texts[0]:
        if len(j) > 3:
          dummy.append(j[3:])
    else:
      dummy.append(i)
  text = dummy
  stopwords = get_stop_words('english') #Getting stopwords from english and indonesian languages
  text = [i for i in text if i not in stopwords] ##Removing stopwords
  wordnet_lemmatizer = WordNetLemmatizer() #Loading Lemmetizer
  text = [wordnet_lemmatizer.lemmatize(word) for word in text] #Lemmetizing the text
  text = " ".join([i for i in text if len(i) < 15]) #Remove the words longer than 15 charecters
  text = "".join([i for i in text if i not in string.punctuation]) #Removing special charecters
  return text

def load_nnlm_model():
    embedding = hub.load("https://www.kaggle.com/models/google/nnlm/TensorFlow2/en-dim128/1")    
    return embedding

def get_knn_model(nnlm):
    
    if use_sql:
        user_products = pd.read_sql(f"SELECT * FROM user_products", conn)
    else:
        user_products = pd.read_csv('user_products.csv')
        
    descriptions = user_products.description.to_list()
    
    embeddings = nnlm(descriptions)
    
    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(embeddings)
    
    return neigh

def get_orders_from_nnlm(text, USER_ID, nnlm, knn):
    
    distance, index = knn.kneighbors(nnlm([text]))
    distance = distance[0][0]
    index = index[0][0]
    
    if use_sql:
        user_products = pd.read_sql(f"SELECT * FROM user_products", conn)
    else:
        user_products = pd.read_csv('user_products.csv')
        
    if(str(USER_ID) == str(user_products.user_id.iloc[index])) and (distance < 1.2):
        return [user_products.order_id.iloc[index]]
    else:
        return []

nnlm = load_nnlm_model()
knn = get_knn_model(nnlm)

