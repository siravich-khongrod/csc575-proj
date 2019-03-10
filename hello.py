import os
from flask import Flask, jsonify, request, send_file, render_template
import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.corpus import stopwords
import requests


import tokenizer
import indexer
import bm25

import imp
#indexer.generate_index()


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def render_sr():
	if 'q' in request.args:
		q = request.args['q']
		url='https://secure-woodland-20008.herokuapp.com/search?q='+q
#	task = [task for task in tasks if task['id'] == task_id]
#    if len(task) == 0:
#        abort(404)
	url='http://127.0.0.1:5000/search?q=i%20love%%20electrical%20engineering'
#	url = 'https://secure-woodland-20008.herokuapp.com/search?q=i%20love%%20electrical%20engineering'
	r = requests.get(url)
	return render_template('search_results.html', results=r.json())


@app.route('/test1', methods=['GET'])
def get_tasks():		
	docs = ['Glimpse is an indexing and query system that allows for search through a file system or document collection quickly. Glimpse is the default search engine in a larger information retrieval system. It has also been used as part of some web based search engines.'
        ,'The main processes in an retrieval system are document indexing, query processing, query evaluation and relevance feedback. Among these, efficient updating of the index is critical in large scale systems.'
        ,'Clusters are created from short snippets of documents retrieved by web search engines which are as good as clusters created from the full text of web documents.']

	docs_token = docs
	for i in range(0,len(docs)):
		docs_token[i] = docs[i].lower()
	porter = nltk.PorterStemmer()
	for i in range(0,3):
		docs_token[i] = word_tokenize(docs_token[i])
		docs_token[i] = [w for w in docs_token[i] if w not in stopwords.words('english')] # filter English stopwords
		docs_token[i] = [porter.stem(tok) for tok in docs_token[i]] # apply stemmer
		docs_token[i] = [w for w in docs_token[i] if w.isalpha()] # filter tokens that contain non-alphabetic character(s)
	if 'id' in request.args:
		id = int(request.args['id'])
		return jsonify({'docs': docs_token[id]})
		
	return jsonify({'docs': docs_token})

@app.route('/search', methods=['GET'])
def search():
	if 'q' in request.args:
		q = request.args['q']
		results = bm25.matching(q)
		return jsonify({'docs': results})
	else:
		return 'error'#jsonify({'docs': bm25.matching('i love python and sql')})


# parse json and create button to download file as hard coded below
@app.route('/get_file', methods=['GET'])
def get_file():
	if 'file' in request.args:
		file = request.args['file']
		return send_file(file,as_attachment=True)
	else:
#		return send_file('data/documents/113183139imran_B.tech_IT.pdf',as_attachment=True)
		return 'file not found error'

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)