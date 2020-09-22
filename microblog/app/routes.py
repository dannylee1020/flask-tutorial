from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
	user = {'username':'Daniel'}
	posts = [
		{
			'author':{'username':'Marius'},
			'body': 'Awesome weather in LA!'
		},
		{
			'author':{'username':'Olivia'},
			'body':'Tenet is such a good movie!'

		}
	]
	return render_template('index.html', title = 'Home', user=user, posts=posts)

