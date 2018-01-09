from app import db
import datetime

class User(db.Model):
  user_id = db.Column(db.String(32), primary_key=True)
  username = db.Column(db.String(32), index=True, unique=True)
  email = db.Column(db.String(128), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  lists = db.relationship('List', backref='author', lazy='dynamic', cascade='all, delete-orphan')
  create_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __repr__(self):
    return '<User {}>'.format(self.username)

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
