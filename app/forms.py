from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.models import User

class LoginForm(Form):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me', default=False)
  submit = SubmitField('Log In')


class RegistrationForm(Form):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  email = StringField('Email', validators=[DataRequired(), Email()])
  email2 = StringField('Repeat Email', validators=[DataRequired(), EqualTo('email')])
  submit = SubmitField('Create Account')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')
