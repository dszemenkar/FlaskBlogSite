from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from blogsite.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
	pass_confirm= PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField('Register')

	def check_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

	def check_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username is already in use.')

class UpdateUserForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update profile')

	def check_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

	def check_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username is already in use.')
