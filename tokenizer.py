import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_token(text):
    #porter = nltk.PorterStemmer()
#    lemmatizer = nltk.WordNetLemmatizer()
    tokens = text.lower() # case-folding (of the whole text string)
    tokens = word_tokenize(tokens) # default tokenizer
    tokens = [w for w in tokens if w not in stopwords.words('english')] # filter English stopwords
    #tokens = [w for w in tokens if len(w) > 2]
    #tokens = [porter.stem(tok) for tok in tokens] # apply stemmer
#    tokens = [lemmatizer.lemmatize(tok) for tok in tokens]
    tokens = [w for w in tokens if w.isalpha()] # filter tokens that contain non-alphabetic character(s)
    return tokens

def tokenize(path):
    text = []
    with open(str(path), 'r') as f:
        for line in f.readlines():
            text.append(line.strip())
    
    # create a list of token
    tokens = [None] * len(text)
    for i in range(len(text)):
        tokens[i] = clean_token(text[i])
    tokens = [t for tok in tokens for t in tok] 
    return tokens