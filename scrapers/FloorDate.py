class FloorDate():
    def __init__(self, proceeding_unix_time=None, proceeding_date=None, add_date=None, 
        duration=None, clip_id=None, mp4_url=None, mp3_url=None, wmv_url=None, events=[]):
        self.proceeding_unix_time = proceeding_unix_time
        self.proceeding_date = proceeding_date
        self.add_date = add_date
        self.duration = duration
        self.clip_id = clip_id
        self.mp4_url = mp4_url
        self.mp3_url = mp3_url
        self.wmv_url = wmv_url
        self.events = events
        
    def save(self):
        ###tie to sqlalchemy
        return None

    def __unicode__(self):
        return self.proceeding_date
        
class FloorEvent():
    def __init__(self, proceeding=None, add_date=None, timestamp=None,
        offset=None, description=None, weight=None, legislation=[]):
        self.proceeding = proceeding
        self.add_date = add_date
        self.timestamp = timestamp
        self.offset = offset
        self.description = description
        self.weight = weight
        self.legislation = legislation
        
    def save(self):
        ###tie to sqlalchemy       
        return None

    def __unicode__(self):
        return self.timestamp