from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

import time
import spacy
from chat import assistant,Web_Search,weather,wiki

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

# Web Scraping Pkg
# from urllib.request import urlopen
from urllib.request import urlopen



@app.route('/')
def index():
	return render_template('button.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	if request.method == 'POST':
		rawtext = request.form['inp']
		ans = assistant(rawtext)
	return render_template('button.html', answer = ans)


@app.route('/about')
def about():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)

#python -m spacy download en
