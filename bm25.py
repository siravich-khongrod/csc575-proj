import math
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

def BM25(doc_len, avg_doc_len, n_doc_w_term, n_total_doc, freq_term_doc, freq_term_query, rel_doc_w_term):
    n = n_doc_w_term
    N = n_total_doc
    f = freq_term_doc
    q = freq_term_query
    r = rel_doc_w_term
    
    p1 = ((k2 + 1) * q) / (k2 + q) #Relevance between term and query
    p2 = ((k1 + 1) * f) / (getK(doc_len, avg_doc_len) + f) #Relevance between term and document
    p3 = math.log((((r + 0.5)/(R-r+0.5)) / ((n - r + 0.5)/(N - n - R + r + 0.5)))+1) # Term Weight
    return p1 * p2 * p3

def getK(doc_len, avg_doc_len):
    return k1 * ((1 - b) + b * (float(doc_len) / float(avg_doc_len)))
    
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# get average document length
def get_avg_doc_len(len_idx):
    _length = 0
    for doc in len_idx:
        _length += len_idx[doc]
    return float(_length) / float(len(len_idx))

def search(query):
    inv_idx_file = open("./data/indexes/inverted_index.json","r")
    inverted_idx = json.load(inv_idx_file)

    len_idx_file = open("./data/indexes/length_index.json","r")
    len_idx = json.load(len_idx_file)

    scores = defaultdict(list)
    
    query_tokens = query.split()
    for token in query_tokens:
    #for token in query:
        if token in inverted_idx.keys():
            for entry in inverted_idx[token]:
                bm25_val = BM25(len_idx[entry[0]],get_avg_doc_len(len_idx),len(inverted_idx[token]),len(len_idx),entry[1],1,0)
                scores[entry[0]] = round(10* sigmoid(bm25_val)-5,4)
    result = sorted(scores.items(),key=operator.itemgetter(1),reverse=True)
    #result = sorted(norm_scores.items(), key = operator.itemgetter(1), reverse = True)
    return result
    
def matching(keyword):
    results = search(keyword)[:5]
    for result in results:
        print(result)
    return results