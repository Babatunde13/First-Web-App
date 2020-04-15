from flask import Flask, render_template, request, url_for, redirect, abort
from forms import RegistrationForm, LoginForm, posts, data, save_db
from hashlib import sha224

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a4c16c8716378db91c1a57bb4cce9183'

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
		for d in data:
			if d['Email'] == user_email and d['Password'] == sha224(request.form['password'].encode('utf-8')).hexdigest():
				user = d['First Name']
				return redirect(url_for('success', name=user))
		else:
			error ='Invalid Email or Password'
			return render_template('login.html', title='Login Page', error=error)
	error=''
	return render_template('login.html', title='Login Page', error=error)



@app.route('/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		user = request.form['First Name']
		print(request.form['password'])
		object_user = {
			'First Name': request.form['First Name'],
			'Last Name': request.form['Last Name'],
			'Email': request.form['email'],
			'Password': sha224(request.form['password'].encode('utf-8')).hexdigest()
		}
		for d in data:
			if d['Email'] == object_user['Email']:
				
				error = 'Already a registered user'
				
				return render_template('login.html', error=error)
		data.append(object_user)
		save_db()

		return redirect(url_for('success', name=user))

	return render_template('signup.html', title='SignUp Page')

@app.route("/register/")
def register():
	form = RegistrationForm()
	return render_template('register.html', title='register', form=form)
 
@app.route("/user/<name>/", methods=['POST', 'GET'])
def success(name):

	if request.method == 'GET':
		for d in data:
			if name == d['First Name']:
				return render_template('success.html', title=f'Welcome {name}', user=name)
			

		return f'<h1> {name} is not registered!</h1>'
	else:
		search = request.form['search']
		search.replace(' ', '+')
		return redirect(f'https://www.google.com/search?q={search}')

if __name__ == '__main__':
	app.run(debug=True)