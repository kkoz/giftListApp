from app import app, db
from app.models import User, List, ListItem, Friendhip

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'List': List,'ListItem':ListItem, 'Friendship':Friendhip}