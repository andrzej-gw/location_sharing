from locationsharinglib import Service
from unidecode import unidecode

import sys
import time
import pyais

data = {
    'mmsi': '30000000',
    'type': 19,
}


cookies_file = 'cookies.txt'
google_email = 'land.rover.discoveryii2002@gmail.com'


while True:
    service = Service(cookies_file=cookies_file, authenticating_account=google_email)
    i=100000
    for person in service.get_all_people():
        #print(person.nickname)
        #print(person.latitude)
        
        data['lat']=person.latitude
        data['lon']=person.longitude
        data['shipname']=unidecode(person.nickname)
        data['mmsi']=str(i)
        i+=1
        encoded = pyais.encode_dict(data, radio_channel="B", talker_id="AIVDM")
        print(encoded[0])
        sys.stdout.flush() 
        #nc -u 0.0.0.0 1234
    time.sleep(15)
