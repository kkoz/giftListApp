from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from .forms import LoginForm, RegistrationForm, EditProfileForm, CreateListForm, AddListItem, ClaimListItem
import uuid
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, List, ListItem
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template('index.html',
                         title='Home',
                         user=current_user)

@app.route('/login', methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html',
                        title='Sign In',
                        form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(user_id=uuid.uuid4().hex, username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations! You are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  posts = [{'author': user, 'body': 'Test Post 1'}, {'author':user, 'body': 'Test Post 2'}]
  return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.',)
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html',
                         title='Edit Profile',
                         form=form)

@app.route('/create_list', methods=['GET','POST'])
@login_required
def create_list():
  form = CreateListForm()
  if form.validate_on_submit():
    list_id = uuid.uuid4().hex
    list = List(list_id=list_id, list_name=form.list_name.data, creator_id=current_user.user_id)
    db.session.add(list)
    db.session.commit()
    flash('List created.')
    return redirect(url_for('edit_list', list_id=list_id))
  return render_template('create_list.html',
                         title='Create List',
                         form=form)

@app.route('/edit_list/<list_id>', methods=['GET','POST'])
@login_required
def edit_list(list_id):
  list = List.query.filter_by(list_id=list_id).first_or_404()
  list_items = ListItem.query.filter_by(list_id=list_id).all()
  if list.creator_id == current_user.user_id:
    form = AddListItem()
    if form.validate_on_submit():
      item = ListItem(list_id=list_id,
                      list_item_id=uuid.uuid4().hex,
                      item_name=form.item_name.data,
                      description=form.description.data,
                      link_url=form.link_url.data)
      db.session.add(item)
      db.session.commit()
      list_items = ListItem.query.filter_by(list_id=list_id).all()
      return render_template("edit_list.html",
                             title='Edit List',
                             list=list,
                             list_items=list_items,
                             form=form)
    return render_template("edit_list.html",
                           title='Edit List',
                           list=list,
                           list_items=list_items,
                           form=form)
  else:
    form = ClaimListItem()
    return render_template('edit_list.html',
                         title='Edit List',
                         form=form)

@app.route('/claim_item/<item_id>', methods=['POST'])
@login_required
def claim_item(item_id):
  print('In AJAX endpoint')
  return jsonify({'successful' : True})