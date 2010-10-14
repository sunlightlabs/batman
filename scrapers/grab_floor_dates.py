#main driver for daily scrape.  scrapes daily meta information for a house proceeding and saves via sqlalchemy if record doesn't already exist

#to-do: tie to sqlalchemy

from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
import datetime, time
from batman.models import FloorEvent, FloorDate, get_or_create_floor_event, get_or_create_floor_date
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
            
            unix_time = cols[0].span.string
            fd = get_or_create_floor_date(unix_time)
            fd.proceeding_unix_time = unix_time
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

            grab_daily_events(fd.proceeding_unix_time)
            
def grab_daily_events(fd_unix_time):
    
    def get_timestamp(item, date, am_or_pm):
        try:
            timestamp = item.nextSibling.nextSibling.a.string
        except:
            timestamp = item.nextSibling.nextSibling.string

        minutes = int(re.findall('(?<=:)\d+', timestamp)[0])
        if re.findall('PM', timestamp):
            hours = int(re.findall('\d+(?=:)', timestamp)[0])
            if hours != 12:
                hours += 12 #convert to 24 clock
            if am_or_pm == 'AM':
                date -= datetime.timedelta(days=1) #we're into the original legislative day now
                am_or_pm = 'PM'
        else: 
            hours = int(re.findall('\d+(?=:)', timestamp)[0])
            if hours == 12:
                hours = 0  #12 am is 0 on 24 hours clock
            am_or_pm = 'AM'
        
        return (datetime.datetime(date.year, date.month, date.day, hours, minutes), date, am_or_pm)

    def parse_group(pt, timestamp, proceeding, offset):
        pt = group.findNext('p')
        weight = 0
        while pt.name == 'p':
            if (len(pt.contents) > 0):
                text = None
                if(len(pt.contents) == 1):
                    text = pt.contents[0]
                else:
                    text = ''.join(pt.findAll(text=True)) #get rid of formatting tags
                    if pt.findAll('a'):
                        pass
                        #need to parse links here
                if text:
                    fe = get_or_create_floor_event(proceeding.proceeding_unix_time, timestamp, weight)
                    fe.add_date = add_date
                    fe.timestamp = timestamp
                    fe.offset = offset
                    fe.description = text.strip()
                    fe.weight = weight
                    weight += 1
                    fe.save()
                else:
                    print "can't parse text "
                    print pt.contents
            if hasattr(pt.nextSibling, 'name'):
                pt = pt.nextSibling
            else:
                break

    proceeding = FloorDate.query.get(fd_unix_time) #FloorDate.query.filter_by(clip_id=clip_id).first() # None #needs completion
    url = "http://houselive.gov/MinutesViewer.php?view_id=2&clip_id=%s&event_id=&publish_id=&is_archiving=0&embedded=1&camera_id=" % proceeding.clip_id
    page = urllib2.urlopen(url).read()
    add_date = datetime.datetime.now()
    soup = BeautifulSoup(page.replace("<p />", "</p><p>"))
    date_field = soup.findAll(text=re.compile('LEGISLATIVE DAY OF'))[0].strip()
    date_string = time.strftime("%m/%d/%Y", time.strptime(date_field.replace('LEGISLATIVE DAY OF ', '').strip(), "%B %d, %Y"))
    groups = soup.findAll('blockquote')
    print proceeding.proceeding_unix_time
    
    try:
        am_or_pm = re.findall('AM|PM|A.M|P.M', groups[0].nextSibling.nextSibling.a.string)[0]
    except Exception:
        print groups[0].nextSibling.nextSibling.string
        am_or_pm = re.findall('AM|PM|A.M|P.M', groups[0].nextSibling.nextSibling.string)[0].replace('.', '')

    if am_or_pm == 'AM': #finishing after midnight, record is being read in backwards
        date = datetime.datetime.fromtimestamp(float(proceeding.proceeding_unix_time)) + datetime.timedelta(days=1)
    else:
        date = datetime.datetime.fromtimestamp(float(proceeding.proceeding_unix_time))

    #special case for first group that's before the first blockquote
    first_group = soup.find('style')
    groups.insert(0, first_group)
    for group in groups:
        if group.nextSibling.nextSibling:
            try:
                offset = int(group.nextSibling.nextSibling.a['onclick'].replace("top.SetPlayerPosition('0:", "").replace("',null); return false;", ""))
            except Exception:
                offset = None
            timestamp, date, am_or_pm = get_timestamp(group, date, am_or_pm)
            desc_group = group#findNext('p')
            parse_group(desc_group, timestamp, proceeding, offset)
        
        else:
            print "no a tag"
            print group.nextSibling
            #print "\n"
                        
grab_daily_meta()
grab_daily_events(1277794800)
