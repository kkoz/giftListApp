from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
import uuid

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname' : 'Kevin'}
	return render_template('index.html',
													title='Home',
													user=user)

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user="%s", remember_me=%s' % (form.username.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html',
												title='Sign In',
												form=form)

@app.route('/create_account', methods=['GET', 'POST'])
def createAcct():
	form = CreateAcctForm()
	if form.validate_on_submit():
		newUuid = uuid.uuid4()
		newUser = models.User(user_id = newUuid.hex,
