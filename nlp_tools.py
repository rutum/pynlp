from shovel import task
from collections import defaultdict
import re
from unidecode import unidecode

spchars = re.compile('\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\+|\=|\\|\||\{|\[|\]|\}|\:|\;|\'|\"|\<|\,|\>|\?|\/|\.|\-')


@task
def normalize(text):
    # convert to unicode
    text = unidecode(text.decode('utf-8', 'ignore'))
    # convert text to lowercase
    text = text.lower()
    # remove special characters
    text = spchars.sub(" ", text)
    return(text)

@task
def word_count(text, wc=None):
    if wc == None:
        wc = defaultdict(int)
    # tokenize by whitespace
    tokens = text.split(" ")
    for t in tokens:
        wc[t] += 1
    return(wc)

@task
def document_frequency(fcount, text, df=None):
    if df == None:
        df = defaultdict(set)
    tokens = text.split(" ")
    for t in tokens:
        print t
        df[t].add(fcount)
    return(df)

@task
def tf_idf(wc, df):
    tfidf = defaultdict(float)
    return(tfidf)
@task
def py_data_seattle_talks(filename):
    import json
    wc = defaultdict(int)
    df = defaultdict(set)
    count = 0
    with open(filename) as fin:
        for line in fin:
            count += 1
            print count
            current = json.loads(line)
            text = normalize(current["description"]+" "+current["title"])
            wc = word_count(text, wc)
            df = document_frequency(count, text, df)
    sorted_wc = sorted(wc.items(), key=lambda x: x[1])
    return sorted_wc, df
