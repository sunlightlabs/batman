from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from local_settings import DATABASE_LOCATION
#from batman_app import db, app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_LOCATION

db = SQLAlchemy()
db.init_app(app)

def create_all_db():
    global db, app
    con = app.test_request_context()
    con.push()
    db.create_all()
    con.pop()

def drop_all_db():
    global db, app
    con = app.test_request_context()
    con.push()
    db.drop_all()
    con.pop()


class FloorDate(db.Model):
    __tablename__ = 'floordate'
    proceeding_unix_time = db.Column(db.Integer, primary_key=True)
    proceeding_date = db.Column(db.Date)
    add_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    clip_id = db.Column(db.Integer)
    mp4_url = db.Column(db.Text)
    mp3_url = db.Column(db.Text)
    wmv_url = db.Column(db.Text)

    def save(self):
        db.session.add(self)
        db.session.commit()

class FloorEvent(db.Model):
    __tablename__ = 'floorevent'
    id = db.Column(db.Integer, primary_key=True)
    proceeding = db.Column(db.ForeignKey(FloorDate.proceeding_unix_time))
    add_date = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime)
    offset = db.Column(db.Integer)
    description = db.Column(db.Text)
    weight = db.Column(db.Integer)
    legislation = db.Column(db.Text)

    def save(self):
        db.session.add(self)
        db.session.commit()
        

def get_or_create_floor_event(proceeding, timestamp, weight):
    current = FloorEvent.query.filter_by(proceeding=proceeding, weight=weight).first()
    if current:
        return current
    else:
        fe = FloorEvent()
        fe.proceeding = proceeding
        fe.timestamp = timestamp
        fe.weight = weight
        return fe
