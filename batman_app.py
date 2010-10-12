from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.xmlrpc import XMLRPCHandler, Fault
from batman.local_settings import DATABASE_LOCATION
from batman.models import FloorDate
import PyRSS2Gen as pyrss
import datetime

DEBUG = True
SECRET_KEY = 'test'

#init app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_LOCATION


#db settings
db = SQLAlchemy()
db.init_app(app)

@app.route('/house')
def house_feed():
    rss_items = []
    for day in FloorDate.query.all():
        day_item = pyrss.RSSItem(
                                title = str(day.proceeding_date),
                                link = day.mp4_url,
                                description = "Legislative Day %s" % day.proceeding_date,
                                guid = pyrss.Guid(day.mp4_url),
                                pubDate = str(day.add_date),
                                )
        rss_items.append(day_item)

    rss = pyrss.RSS2(
                    title = "HouseLive.gov Video",
                    link = "http://batman.sunlightlabs.com/house",
                    description = "HouseLive.gov Video Feed",
                    lastBuildDate = datetime.datetime.now(),
                    items = rss_items
                    )
    return rss.to_xml()
@app.route('/')
def home():
    my_str = ''
    for fd in FloorDate.query.all():
        my_str += '\n' + str(fd.clip_id)

    return my_str
    return 'test'


if __name__ == '__main__':
    app.run()

