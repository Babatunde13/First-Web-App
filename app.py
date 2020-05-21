from flask import Flask, render_template, request, url_for, redirect, abort, flash
from forms import RegistrationForm, LoginForm, posts, data, save_db
from hashlib import sha224
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SECRET_KEY'] = 'a4c16c8716378db91c1a57bb4cce9183'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHMEY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	email = db.Column(db.String(64))
	password = db.Column(db.String(20))

	def __repr__(self):
		return f'<user {self.name}>'

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html')


@app.route('/about/')
def about():
	return render_template('about.html', posts=posts, title='About Page')

@app.route('/login/', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		user_email = request.form['email']
		user = User.query.filter_by(email=user_email, password=sha224(request.form['password'].encode('utf-8')).hexdigest()).first()
		if user is None:
			flash('Inavlid email or password')
			return render_template('login.html', title='Login Page')
		return redirect(url_for('success', name=user.name))
	return render_template('login.html', title='Login Page')



@app.route('/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		user = User(name=request.form['First Name']+' '+request.form['Last Name'], email=request.form['email'], password=sha224(request.form['password'].encode('utf-8')).hexdigest())
		check = User.query.filter_by(email=user.email)
		if check is not None:
			db.session.add(user)
			db.session.commit()
			print(user.name)
			return redirect(url_for('success', name=user.name))
		flash('Already a registered user,  Login!')
		return render_template('login.html')
	return render_template('signup.html', title='SignUp Page')

@app.route("/register/")
def register():
	form = RegistrationForm()
	return render_template('register.html', title='register', form=form)
 
@app.route("/user/<name>/", methods=['POST', 'GET'])
def success(name):
	if request.method == 'GET':
		check = User.query.filter_by(name=name)
		if name is not None:
			return render_template('success.html', title=f'Welcome {name}', user=name)
			

		return redirect(url_for('login'))
	else:
		search = request.form['search']
		search.replace(' ', '+')
		return redirect(f'https://www.google.com/search?q={search}')

if __name__ == '__main__':
	app.run(debug=True)