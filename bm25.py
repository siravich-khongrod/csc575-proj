from math import log
from collections import defaultdict
import json
import operator

'''
IR Book: 11.4.3
Fomula: 11.33
'''
'''
typical TREC value
f1 = 1.2
k2 varies from 0 to 1000
b = 0.75
'''

k1 = 1.2
b = 0.75
k2 = 100
R = 0 # (set to 0 if no relevancy info is known)

# MAIN METHOD

def BM25(docLen, avDocLen, n, N, f, q, r):
    p1 = ((k2 + 1) * q) / (k2 + q)
    p2 = ((k1 + 1) * f) / (getK(docLen, avDocLen) + f)
    p3 = log(((r + 0.5)/(R-r+0.5)) / ((n - r + 0.5)/(N - n - R + r + 0.5)))
    return p1 * p2 * p3

def getK(docLen, avDocLen):
    return k1 * ((1 - b) + b * (float(docLen) / float(avDocLen)))
	
	
# get average document length
def get_avdl(length_index):
    corpus_length = 0
    for document in length_index:
        corpus_length += length_index[document]
    return float(corpus_length) / float(len(length_index))

def search(query):
    inv_index_file = open("./data/indexes/inverted_index.json","r")
    inverted_index = json.load(inv_index_file)

    length_index_file = open("./data/indexes/length_index.json","r")
    length_index = json.load(length_index_file)

    scores = defaultdict(list)
    
    #query_tokens = query.split()
    #for token in query_tokens:
    for token in query:
        if token in inverted_index.keys():
            for entry in inverted_index[token]:
                scores[entry[0]] = BM25(length_index[entry[0]],get_avdl(length_index),len(inverted_index[token]),len(length_index),entry[1],1,0)
    return sorted(scores.items(),key=operator.itemgetter(1),reverse=True)
	
def matching(keyword):
    results = search(keyword)
    return results