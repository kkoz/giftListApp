from app import db, login
import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
  user_id = db.Column(db.String(32), primary_key=True)
  username = db.Column(db.String(32), index=True, unique=True)
  email = db.Column(db.String(128), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  lists = db.relationship('List', backref='author', lazy='dynamic', cascade='all, delete-orphan')
  create_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __repr__(self):
    return '<User {}>'.format(self.username)
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  def get_id(self):
    return self.user_id
  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

@login.user_loader
def load_user(user_id):
  return User.query.get(user_id)

class List(db.Model):
  list_id = db.Column(db.String(32), primary_key=True)
  list_name = db.Column(db.String(32), index=True)
  creator_id = db.Column(db.String(32), db.ForeignKey('user.user_id'))
  items = db.relationship('ListItem', backref='list', lazy='dynamic', cascade='all, delete-orphan')
  create_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  def __repr__(self):
    return '<List {}>'.format(self.list_name)


class ListItem(db.Model):
  list_id = db.Column(db.String(32), db.ForeignKey('list.list_id'))
  list_item_id = db.Column(db.String(32), primary_key=True)
  item_name = db.Column(db.String(64),index = True)
  description = db.Column(db.String(256))
  link_url = db.Column(db.String(256))
  purchaser_id = db.Column(db.String(32), db.ForeignKey('user.user_id'))
  create_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  def __repr__(self):
    return '<ListItem {}>'.format(self.item_name)

class Friendhip(db.Model):
  friendship_id = db.Column(db.String(32), primary_key=True)
  user_id_1 = db.Column(db.String(32), db.ForeignKey('user.user_id'), index=True)
  user_id_2 = db.Column(db.String(32), db.ForeignKey('user.user_id'), index=True)
  create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  def __repr__(self):
    return '<Friendship {}, {}>'.format(self.user_id_1, self.user_id_2)
