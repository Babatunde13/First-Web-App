from flask import Flask, render_template, request, url_for, redirect, abort, flash
from forms import RegistrationForm, LoginForm, posts
from hashlib import sha224
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SECRET_KEY'] = 'a4c16c8716378db91c1a57bb4cce9183'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHMEY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	FirstName = db.Column(db.String(64), index=True)
	LastName = db.Column(db.String(64), index=True)
	email = db.Column(db.String(64))
	password = db.Column(db.String(20))

	def __repr__(self):
		return f'<user {self.FirstName} {self.LastName}>'

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
		user = User.query.filter_by(email=user_email).first()
		if user is None:
			flash('Inavlid email sign up first')
			return render_template('signup.html', title='Signup Page')
		if check_password_hash(user.password, request.form['password']):
			return redirect(url_for('success', name=user.FirstName))
		flash('Invalid email or password')
	return render_template('login.html', title='Login Page')



@app.route('/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		user = User(FirstName=request.form['First Name'], LastName=request.form['Last Name'], email=request.form['email'], password=generate_password_hash(request.form['password']))
		check = User.query.filter_by(email=user.email, password=user.password)
		if check is not None:
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('success', name=user.FirstName))
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
		check = User.query.filter_by(FirstName=name).first()
		if name is not None:
			return render_template('success.html', title=f'Welcome {name}', user=name)
		return redirect(url_for('login'))
	else:
		search = request.form['search']
		search.replace(' ', '+')
		return redirect(f'https://www.google.com/search?q={search}')

if __name__ == '__main__':
	app.run(debug=True)