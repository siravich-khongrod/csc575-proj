import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_token(text):
    #porter = nltk.PorterStemmer()
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = text.lower() # case-folding (of the whole text string)
    tokens = word_tokenize(tokens) # default tokenizer
    tokens = [w for w in tokens if w not in stopwords.words('english')] # filter English stopwords
    #tokens = [w for w in tokens if len(w) > 2]
    #tokens = [porter.stem(tok) for tok in tokens] # apply stemmer
    tokens = [lemmatizer.lemmatize(tok) for tok in tokens]
    tokens = [w for w in tokens if w.isalpha()] # filter tokens that contain non-alphabetic character(s)
    return tokens

def tokenize(path):
    # open PDF
    pdf = PyPDF2.PdfFileReader(open(str(path),"rb"))
    stopword_list = list(stopwords.words("english"))

    # read PDF file in a list
    pdf_content = []
    for page in pdf.pages:
        pdf_content.append(page.extractText())
    
    # create a list of token
    tokens = [None] * len(pdf_content)
    for i in range(len(pdf_content)):
        tokens[i] = clean_token(pdf_content[i])
    tokens = [t for tok in tokens for t in tok] 
    return tokens