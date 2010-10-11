from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

DEBUG = True
SECRET_KEY = 'test'

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_LOCATION
db = SQLAlchemy(app)

@app.route('/')
def home():
    return 'test'

@app.after_request
def shutdown_session(response):
    db_session.remove()
    return response



if __name__ == '__main__':
    app.run()

