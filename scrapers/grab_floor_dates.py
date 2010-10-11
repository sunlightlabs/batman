from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
import datetime, time
import urllib2
import re

class FloorDate():
    def __init__(self, proceeding_unix_time=None, proceeding_date=None, add_date=None, 
        duration=None, clip_id=None, mp4_url=None, mp3_url=None, wmv_url=None):
        self.proceeding_unix_time = proceeding_unix_time
        self.proceeding_date = proceeding_date
        self.add_date = add_date
        self.duration = duration
        self.clip_id = clip_id
        self.mp4_url = mp4_url
        self.mp3_url = mp3_url
        self.wmv_url = wmv_url
        
    def __unicode__(self):
        return self.proceeding_date
        
def convert_duration(hours, minutes):
    hours = int(hours)
    minutes = int(minutes)
    total_mins = (hours * 60) + minutes
    return total_mins

def locate_clip_id(url):
    clip_id = None
    params = urlparse(url)[4].split('&')
    for param in params:
        if param.split('=')[0] == 'clip_id':
            clip_id = param.split('=')[1]
    return int(clip_id)
        
url = "http://houselive.gov/ViewPublisher.php?view_id=14"
page = urllib2.urlopen(url)
add_date = datetime.datetime.now()
soup = BeautifulSoup(page)
link = soup.find('table', id="archive")

rows = link.findAll('tr')
for row in rows:
    cols = row.findAll('td')
    if len(cols) > 0:
        fd = FloorDate()
        fd.proceeding_unix_time = cols[0].span.string
        fd.proceeding_date = cols[0].contents[1]
        fd.add_date = add_date
        duration_hours = cols[1].contents[0]
        duration_minutes = cols[1].contents[2].replace('&nbsp;', '')
        fd.duration = convert_duration(duration_hours, duration_minutes)
        fd.clip_id = locate_clip_id(cols[3].contents[2]['href'])
        fd.mp3_url = cols[4].a['href']
        fd.mp4_url = fd.mp3_url.replace('.mp3', '.mp4')
        fd.wmv_url = fd.mp3_url.replace('.mp3', '.wmv')