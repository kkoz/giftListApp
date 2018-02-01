from app import app
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

if not app.debug:
  if app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
      auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
      secure = ()
    mail_handler = SMTPHandler(
      mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
      fromaddr='no-reply@' + app.config['MAIL_SERVER'],
      toaddrs=app.config['ADMINS'], subject='Gift List App Failure',
      credentials=auth, secure=secure
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
      os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/giftListApp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Gift List App Startup')