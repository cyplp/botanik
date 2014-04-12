""" Cornice services.
"""
from cornice import Service
from datetime import datetime
import sqlite3


door = Service(name='door', path='/', description="Door app")

class door_state(object):
    
    def __init__(self):
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.state = 'Unknow'
        self.lastchange = now

mydoor = door_state()

@door.get()
def get_info(request):
    """Returns state of door lock."""
    return {
            'state' : mydoor.state,
            'lastchange' : mydoor.lastchange
            }

@door.post()
def post_info(request):
    """Post State door"""
    data = request.POST.mixed()
    mydoor.state = data['state']
    mydoor.lastchange = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return {
            'state' : mydoor.state,
            'lastchange' : mydoor.lastchange
            }

