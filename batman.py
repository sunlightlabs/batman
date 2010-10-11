from batman.database import db_session
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

DEBUG = True
SECRET_KEY = 'test'


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG

@app.route('/')
def home():
    return 'test'

if __name__ == '__main__':
    app.run()

