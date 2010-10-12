#main driver for daily scrape.  scrapes daily meta information for a house proceeding and saves via sqlalchemy if record doesn't already exist

#to-do: tie to sqlalchemy

from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
import datetime, time
from FloorDate import FloorDate, FloorEvent
import urllib2
import re
        
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
            
def grab_daily_meta():
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
            fd.proceeding_date = time.strftime('%Y-%m-%d', time.strptime(cols[0].contents[1], '%B %d, %Y'))
            fd.add_date = add_date
            duration_hours = cols[1].contents[0]
            duration_minutes = cols[1].contents[2].replace('&nbsp;', '')
            fd.duration = convert_duration(duration_hours, duration_minutes)
            fd.clip_id = locate_clip_id(cols[3].contents[2]['href'])
            fd.mp3_url = cols[4].a['href']
            fd.mp4_url = fd.mp3_url.replace('.mp3', '.mp4')
            fd.wmv_url = fd.mp3_url.replace('.mp3', '.wmv')
            fd.save()
            
def grab_daily_events(clip_id):
    url = "http://houselive.gov/MinutesViewer.php?view_id=2&clip_id=%s&event_id=&publish_id=&is_archiving=0&embedded=1&camera_id=" % clip_id
    page = urllib2.urlopen(url)
    add_date = datetime.datetime.now()
    soup = BeautifulSoup(page)
    print soup.prettify()
    date_field = soup.findAll(text=re.compile('LEGISLATIVE DAY OF'))[0].strip()
    date_string = time.strftime("%m/%d/%Y", time.strptime(date_field.replace('LEGISLATIVE DAY OF ', '').strip(), "%B %d, %Y"))
    groups = soup.findAll('blockquote')

    proceeding = None #needs completion
    for group in groups:
        if group.nextSibling.nextSibling:
            timestamp = None #needs completion
            offset = int(group.nextSibling.nextSibling.a['onclick'].replace("top.SetPlayerPosition('0:", "").replace("',null); return false;", ""))
            print "offset: %s" % offset
            fe = FloorEvent()
            fe.add_date = add_date
            fe.timestamp = timestamp
            fe.offset = offset
            desc_group = group.findNext('p')
            
            pt = group.findNext('p')
            while pt.name == 'p':
                if (len(pt.contents) > 0):
                    print(pt.contents[0])
                if hasattr(pt.nextSibling, 'name'):
                    pt = pt.nextSibling
                else:
                    break
        print "\n"
                        
#grab_daily_meta()
grab_daily_events(4679)