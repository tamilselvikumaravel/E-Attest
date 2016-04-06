

from new import *
from paralellfr import *
from flask import Flask,render_template,redirect,url_for,request

app = Flask(__name__)

@app.route('/')
def display():
	return render_template('pg.html')
	
@app.route('/dis',methods=['POST'])
def dis():	
	if request.method=='POST':
		if request.form['search'] == 'basicsearch':
			ss=request.form['url']
			#max_pages=int(request.form['max_pages'])
			#max_pages=2
			crawled,t1,length,t2,ranks,graph,m=display_search(ss)
			return render_template('pg.html',crawled=crawled,t1=t1,length=length,rank_time=t2)
		elif request.form['search'] == 'parallel':
			ss=request.form['url']
			console_index,t,lenseed,rank_time=xy(ss)
			return render_template('pg.html',crawled=console_index,t1=t,length=lenseed,rank_time=rank_time)
	
	
if __name__=='__main__':
	app.run(debug=True)

	

