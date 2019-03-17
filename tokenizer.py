import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

###########################################################################
def convert(file):
    text = []
    with open(str(file), 'rb') as f:
        for line in f.readlines():
            text.append(line.decode("utf-8", "ignore").strip())
    return text

###########################################################################     
def tokenize(lst):            
    # create a list of token
    
    tokens = [None] * len(lst)
    for i in range(len(lst)):
        tokens[i] = clean_token(lst[i])
    tokens = [t for tok in tokens for t in tok] 
    return tokens

########################################################################### 
def clean_token(text):
    #porter = nltk.PorterStemmer()
    lemmatizer = nltk.WordNetLemmatizer()
    #snowball = nltk.SnowballStemmer('english')
        
    stopset = set(stopwords.words('english'))
    stopset.update(('less','year'))
    
    noun_lst = []

    for word,tag in (TextBlob(text).tags):
        if tag in ("NN", "NNS", "NNP", "NNPS","JJ"):
            word = word.lower()
            word = lemmatizer.lemmatize(word)
            #word = porter.stem(word)
            #word = snowball.stem(word)
            if word not in stopset and word.isalpha() and len(word)>2:
                noun_lst.append(word)
    return noun_lst
