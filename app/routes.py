from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from sqlalchemy import and_
from .forms import LoginForm, RegistrationForm, EditProfileForm,\
  CreateListForm, AddListItem, ClaimListItem, AddListPermission
import uuid
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, List, ListItem, ListPermission
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

@app.route('/my_lists')
@login_required
def my_lists():
  my_lists = List.query.filter_by(creator_id=current_user.user_id).all()
  lists_permissions = ListPermission.query.filter_by(user_id=current_user.user_id).all()
  list_ids = list(map(lambda perm: perm.list_id, lists_permissions))

  lists_with_permission = List.query.filter(List.list_id.in_(list_ids)).all()
  return render_template('my_lists.html',
                         my_lists=my_lists,
                         lists_with_permission=lists_with_permission)

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
    add_item_form = AddListItem()
    if add_item_form.validate_on_submit():
      print("Submitted add_item_form")
      item = ListItem(list_id=list_id,
                      list_item_id=uuid.uuid4().hex,
                      item_name=add_item_form.item_name.data,
                      description=add_item_form.description.data,
                      link_url=add_item_form.link_url.data)
      db.session.add(item)
      db.session.commit()
      list_items = ListItem.query.filter_by(list_id=list_id).all()
      return render_template("edit_list.html",
                             title='Edit List',
                             list=list,
                             list_items=list_items,
                             add_item_form=add_item_form,
                             user_id=current_user.user_id)

    return render_template("edit_list.html",
                           title='Edit List',
                           list=list,
                           list_items=list_items,
                           user_id=current_user.user_id,
                           add_item_form=add_item_form)
  else:
    permitted_users = ListPermission.query.filter_by(list_id=list_id).all()
    this_user_list = [user for user in permitted_users if user.user_id == current_user.user_id]
    print("This user's ID: {}".format(current_user.user_id))
    print("Permitted user's IDs")
    for user in permitted_users:
      print(user.user_id)
    if len(this_user_list) > 0:
      return render_template('edit_list.html',
                             list=list,
                             list_items=list_items,
                             user_id=current_user.user_id,
                             title='Edit List')
    else:
      flash("You are not permitted to edit this list")
      return redirect(url_for('index'))

@app.route('/add_list_permission/<list_id>', methods=['GET','POST'])
@login_required
def add_list_permission(list_id):
  list = List.query.filter_by(list_id=list_id).first_or_404()
  permissions = ListPermission.query.filter_by(list_id=list_id).all()
  list_permission_form = AddListPermission()
  if list_permission_form.validate_on_submit():
    print("submitted list_permission_form")
    user_to_add = User.query.filter_by(username=list_permission_form.username.data).first()
    if user_to_add is not None:
      permission = ListPermission(list_id=list_id,
                                  user_id=user_to_add.user_id,
                                  list_permission_id=uuid.uuid4().hex)
      db.session.add(permission)
      db.session.commit()
      flash("Granted user '{}' permissions on list".format(user_to_add.username))
      permissions = ListPermission.query.filter_by(list_id=list_id).all()
      return render_template("add_list_permission.html",
                             title='Edit List',
                             list=list,
                             permissions=permissions,
                             list_permission_form=list_permission_form)
    else:
      print("User '{}' does not exist".format(list_permission_form.username.data))
      flash("User '{}' does not exist".format(list_permission_form.username.data))
  return render_template("add_list_permission.html",
                             title='Edit List',
                             list=list,
                             list_permission_form=list_permission_form)

@app.route('/claim_item/<item_id>', methods=['POST'])
@login_required
def claim_item(item_id):
  list_item = ListItem.query.filter_by(list_item_id=item_id).first()
  print("claim_item for item {}".format(list_item.list_item_id))
  payload = request.get_json()
  print(payload)
  if list_item is not None:
    #Check if user is permitted to edit list
    permission = ListPermission.query.filter_by(list_id=list_item.list_id).first()
    if permission is not None:
      #Check if the item has been claimed
      print("User has permission")
      if list_item.purchaser_id is None:
        print("no current purchaser")
        if payload['claim'] != "true":
          list_item.purchaser_id = current_user.user_id
          db.session.commit()
          return jsonify({'claim_successful': True})
        else:
          return jsonify({'claim_successful': False, 'message': "Cannot unclaim item you have not claimed"})
      else:
        if list_item.purchaser_id == current_user.user_id:
          if payload['claim'] == 'true':
            return jsonify({'claim_successful': False, 'message': "You've already claimed this item."})
          else:
            #Unclaim the item
            list_item.purchaser_id = None
            db.session.commit()
            return jsonify({'claim_successful': True, 'message': "Successfully unclaimed the item."})
        #Someone else has claimed it
        print("Someone else has claimed this")
        return jsonify({'claim_successful' : False, 'message': 'Item is already claimed'})
    else:
      print("No permission to edit")
      return jsonify({'claim_successful': False, 'message': "User doesn't have permissions on this list"})
  else:
    return jsonify({'claim_successful': False, 'message': "List does not exist"})

@app.route('/test')
def test():
  return render_template("test.html")

@app.route('/list_items/<list_id>')
@login_required
def list_items(list_id):
  permitted_user = ListPermission.query.filter(and_(ListPermission.list_id == list_id, ListPermission.user_id == current_user.user_id)).first()
  list_owner = List.query.filter_by(creator_id=current_user.user_id).first()
  if(permitted_user is not None or (list_owner is not None and list_owner == current_user.user_id)):
    list_items = ListItem.query.filter_by(list_id=list_id).all()
    jsonable_items = list(map(lambda item: item.to_dict(), list_items))
    return jsonify({'status': 'Successful', 'items': jsonable_items})
  else:
    response = jsonify({'status': 'Failure: User Not Authorized'})
    response.status_code = 403
    return response