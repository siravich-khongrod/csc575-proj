import glob
from collections import defaultdict
import tokenizer
import imp
import json
#imp.reload(tokenizer)

def get_file_names():
    files = []
    #'../data/solarhrm*.pdf'
    for file in glob.glob("./data/documents/*.txt"):
        files.append(file)
    return files

def make_index(tokens, document_name, index, length):
    for term in set(tokens):
        index[term].append([document_name,tokens.count(term)])
        length[document_name] = len(set(tokens))

def write(inverted_index,length_index):
    inv_index_file = open("./data/indexes/inverted_index.json","w")
    json.dump(inverted_index,inv_index_file)

    length_index_file = open("./data/indexes/length_index.json","w")
    json.dump(length_index,length_index_file)
    
def generate_index():
    print('generating index...')
    resume_files = get_file_names()
    inverted_index = defaultdict(list)
    length_index = defaultdict(list)
    f = open("./logs",'w')
    for file in resume_files:
        try:
            file = tokenizer.convert(file)
            make_index(tokenizer.tokenize(file), file, inverted_index, length_index)
        except:
            print("warning: "+file+" not indexed")
            f.write(file+'\n')
    f.close()
    write(inverted_index,length_index)
    print ("Indexes generated")
