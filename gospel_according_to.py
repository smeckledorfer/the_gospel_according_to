import streamlit as st

from freebible import read_web
from freebible import bibles
web = read_web()

import string

with open("C:\\Users\\Matthew\\streamlit_apps\\gatsby.txt",'r',encoding = "utf-8") as file:
    text = file.readlines()

text = " ".join(text)


st.title("Welcome, beautiful person!")

st.subheader("What is your name?")
name = st.text_input('What is your name?')

st.write("")

name_sentence = "Hello, " + name + "! What story would you like to be in?"
st.subheader(name_sentence)

#book  = st.multiselect('Choose your book...', ['Gen', 'Exo', 'Lev', 'Num', 'Deu'])
book = st.selectbox('Choose your book...', ['Gen', 'Exo', 'Lev','Num', 'Deu'])
#book = book[0]

chapter  = st.number_input('Pick a chapter...', 0, 10)

verse  = st.number_input('Pick a verse...', 0, 10)
#"""
import stanza as sz
sz.download('en')
sz.install_corenlp()
nlp = sz.Pipeline('en')
from stanza.server import CoreNLPClient
#"""

st.write(text)

#text = str(bibles.web.quote(book, chapter, verse)).split("]")[1].replace("'","").strip(",").strip('"')



def annotate(text):
    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
            timeout=30000000,
            memory='6G', output_format="json") as client:
        annotation = client.annotate(text)
    return annotation

ann_json = annotate(text)
#For Story of Us implemention, define a function to check for and return the chain with the proper entity reference


st.write(ann_json['corefs'])
st.write(text)


chain_selector = 1

for r in range(len(sorted(ann_json['corefs'].items())[chain_selector][1])-1):
    sentence_key = sorted(ann_json['corefs'].items())[chain_selector][1][r]['position'][0]
    token_key = sorted(ann_json['corefs'].items())[chain_selector][1][r]['position'][1]

    ann_json['sentences'][sentence_key-1]['tokens'][token_key-1]['word'] = name

gospel = ""
for i in range(len(ann_json['sentences'])):
        for j in range(len(ann_json['sentences'][i]['tokens'])):
            gospel = gospel + ann_json['sentences'][i]['tokens'][j]['word'] + " "
st.write(gospel)
