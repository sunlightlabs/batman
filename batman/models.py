from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from local_settings import DATABASE_LOCATION
from batman import db, app

class TimestampLink(db.Model):
    __tablename__ = 'timestamplink'
    id = db.Column(db.Integer, primary_key=True)
    clip_id = db.Column(db.Integer)
    offset = db.Column(db.Integer)

    def __init__(self, clip_id=None, offset=None):
        self.clip_id = clip_id
        self.offset = offset

    def __repr__(self):
        return "<TimestampLink clip_id:%r offset:%r>" % (self.clip_id, self.offset)
