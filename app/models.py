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
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
  permissions = db.relationship('ListPermission', backref='list', lazy='dynamic', cascade='all, delete-orphan')
  def __repr__(self):
    return '<List {}>'.format(self.list_name)

class ListPermission(db.Model):
  list_permission_id = db.Column(db.String(32), primary_key=True)
  list_id = db.Column(db.String(32), db.ForeignKey('list.list_id'))
  user_id = db.Column(db.String(32), db.ForeignKey('user.user_id'))
  def __repr__(self):
    return '<ListPermission {} -> {}>'.format(self.user_id, self.list_id)


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
  def to_dict(self):
    return {
      "list_id": self.list_id,
      "list_item_id": self.list_item_id,
      "item_name": self.item_name,
      "description": self.description,
      "link_url": self.link_url,
      "purchaser_id": self.purchaser_id,
      "create_timestamp": self.create_timestamp
    }

class Friendhip(db.Model):
  friendship_id = db.Column(db.String(32), primary_key=True)
  user_id_1 = db.Column(db.String(32), db.ForeignKey('user.user_id'), index=True)
  user_id_2 = db.Column(db.String(32), db.ForeignKey('user.user_id'), index=True)
  create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  def __repr__(self):
    return '<Friendship {}, {}>'.format(self.user_id_1, self.user_id_2)
