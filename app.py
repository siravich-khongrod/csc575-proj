import os
from flask import Flask, jsonify, request, send_file, render_template, abort
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
		if len(q) == 0:
			abort(404)
		url=request.base_url+'search_api?q='+q
		print(url)
	else:
		abort(404)
#	url='https://secure-woodland-20008.herokuapp.com/search?q='+q
#	task = [task for task in tasks if task['id'] == task_id]
#    if len(task) == 0:
#        abort(404)
#	url='http://127.0.0.1:5000/search_api?q=i%20love%%20electrical%20engineering'
#	url = 'https://secure-woodland-20008.herokuapp.com/search?q=i%20love%%20electrical%20engineering'
	r = requests.get(url)
	return render_template('search_results.html', results=r.json())

@app.route('/search_api', methods=['GET'])
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
		abort(404)
		return 'file not found error'

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)