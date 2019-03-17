#import os
#from flask import Flask, jsonify, request, send_file, render_template, abort
import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.corpus import stopwords

import tokenizer
import indexer
import bm25

# Create index
indexer.generate_index()

# Retrieve results
results = bm25.matching('i love drinking beer')
jsonify({'docs': results})
