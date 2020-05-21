from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
import json


class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""

	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	"""docstring for LoginForm"""

	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
	
posts = [
	{
		'author': 'Corey Schafer',
		'title': 'Blog Post 1',
		'content': 'Blog Post',
		'date_posted': 'April 20, 2018'
	},
	{
		'author': 'Babatunde Koiki',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': 'April 21, 2018'
	},
	{
		'author': 'Sodiq Agunbiade',
		'title': 'Blog Post 3',
		'content': 'Third post content',
		'date_posted': 'April 22, 2018'
	},
	{
		'author': 'Sodiq Akinjobi',
		'title': 'Blog Post 4',
		'content': 'Fourth post content',
		'date_posted': 'April 23, 2018'
	}
]
