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
        # Uncomment if you want to remove stopwords
        # if not is_stopword(t):
        #     wc[t] += 1
        wc[t] += 1  # comment, if stopwords are being removed
    return(wc)

def document_frequency(f_id, text, df=None):
    if df == None:
        df = defaultdict(set)
    tokens = text.split(" ")
    for t in tokens:
        df[t].add(f_id)
    return(df)

def inversedf(w, df, count):
    nonlog = count/len(df[w])
    if nonlog <= 0:
        return 0.00001
    else:
        return math.log(nonlog)

def bulk_idf(wc, df, count):
    idf = defaultdict(int)
    for w in wc:
        idf[w] = math.log(count/len(df[w]))
    return idf

def tf_idf(wc, df, count):
    tfidf = defaultdict(float)
    for w in wc:
        tfidf[w] = wc[w] * inversedf(w, df, count)
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
    import numpy
    import json
    wc = defaultdict(int)
    df = defaultdict(set)
    count = 0
    # first compute the global IDF

    with open(filename) as fin:
        for line in fin:
            count += 1
            current = json.loads(line)
            text = normalize(current["abstract"] + " " + \
                current["description"] + " " + current["title"])
            wc = word_count(text, wc)
            df = document_frequency(count, text, df)
    numdocs = count
    idf = bulk_idf(wc, df, numdocs)

    #initialize an numpy array with zeros
    docvec = numpy.zeros(shape=(count, len(wc)), dtype=float)

    # compute an index
    count = 0
    word2index = {}
    for w in wc:
        word2index[w] = count
        count+=1

    count = 0
    with open(filename) as fin:
        for line in fin:
            current = json.loads(line)
            text = normalize(current["abstract"] + " " + \
                current["description"] + " " + current["title"])
            wc = word_count(text, wc)
            tfidf = tf_idf(wc, df, count)# build vocabulary
            for token in tfidf:
                docvec[count, word2index[token]] = tfidf[token]
            count += 1
    return docvec, idf, word2index, numdocs

model, idf, word2id, numdocs = build_search_model(filename)

def search(phrase, idf, word2id, numdocs, model):
    wc = defaultdict(int)
    wc = word_count(phrase, wc)
    docvec = numpy.zeros(shape=(1, len(idf)), dtype=float)
    tfidf = tf_idf(wc, df, numdocs)# build vocabulary
    for token in tfidf:
        docvec[0, word2index[token]] = tfidf[token]

    max_sim = -99
    index = -99
    count=0
    for m in model:
        sim = similarity(m, docvec[0])
        if max_sim == -99:
            max_sim = sim
            index = count
        else:
            if max_sim < sim:
                max_sim = sim
                index = count
        count+=1
    return max_sim, index
