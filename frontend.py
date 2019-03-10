from flask import Flask, request, abort, render_template, send_file
import requests

app = Flask(__name__,template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def render_sr():
	if 'q' in request.args:
		q = request.args['q']
		url='https://secure-woodland-20008.herokuapp.com/search?q='+q
#	task = [task for task in tasks if task['id'] == task_id]
#    if len(task) == 0:
#        abort(404)
#	url = 'https://secure-woodland-20008.herokuapp.com/search?q=i%20love%%20electrical%20engineering'
	r = requests.get(url)
	return render_template('search_results.html', results=r.json())
    #return jsonify({'sr': content})
	
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