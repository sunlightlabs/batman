from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flaskext.sqlalchemy import SQLAlchemy
from batman.local_settings import DATABASE_LOCATION

DEBUG = True
SECRET_KEY = 'test'

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_LOCATION
db = SQLAlchemy()
db.init_app(app)

@app.route('/')
def home():
    return 'test'


if __name__ == '__main__':
    app.run()

