from collections import defaultdict
import re
from unidecode import unidecode
import math

spchars = re.compile('\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\+|\=|\\|\||\{|\[|\]|\}|\:|\;|\'|\"|\<|\,|\>|\?|\/|\.|\-')


def load_stopwords(filename):
    stopwords = set()
    with open(filename, "r") as fin:
        for line in fin:
            tok = line.strip()
            stopwords.add(tok.lower())
    return(stopwords)

stopwords = load_stopwords("stopwords.txt")

def is_stopword(token):
    if token in stopwords:
        return(True)
    else:
        return(False)

def normalize(text):
    # convert to unicode
    text = unidecode(text.decode('utf-8', 'ignore'))
    # convert text to lowercase
    text = text.lower()
    # remove special characters
    text = spchars.sub(" ", text)
    return(text)

def word_count(text, wc=None):
    if wc == None:
        wc = defaultdict(int)
    # tokenize by whitespace
    tokens = text.split(" ")
    for t in tokens:
        if not is_stopword(t):
            wc[t] += 1
    return(wc)

def document_frequency(f_id, text, df=None):
    if df == None:
        df = defaultdict(set)
    tokens = text.split(" ")
    for t in tokens:
        df[t].add(f_id)
    return(df)

def tf_idf(wc, df, count):
    tfidf = defaultdict(float)
    for w in wc:
        tfidf[w] = wc[w] * math.log(count/len(df[w]))
    return(tfidf)

def information_extraction(filename):
    import json
    wc = defaultdict(int)
    df = defaultdict(set)
    count = 0
    with open(filename) as fin:
        for line in fin:
            count += 1
            current = json.loads(line)
            text = normalize(current["abstract"] + " " + \
                current["description"] + " " + current["title"])
            wc = word_count(text, wc)
            df = document_frequency(count, text, df)
    tfidf = tf_idf(wc, df, count)
    # sorted_wc = sorted(wc.items(), key=lambda x: x[1])
    return wc, df, tfidf

def similarity(vector1, vector2):
    score = sum(p*q for p,q in zip(vector1, vector2))/(math.sqrt(sum(i**2 for i in vector1))*math.sqrt(sum(i**2 for i in vector2)))
    return score

def build_search_model(filename):
    # build vocabulary
    # for each document:
    #   compute TF
    #   compute IDF
    #   update document vector
    # return the list of vectors

model = build_search_model(filename)

def search(phrase):
    # build TF*IDF vector for the search phrase
    # for each document:
    #   compute similarity between phrase and document
    # return the document with highest similarity with phrase

