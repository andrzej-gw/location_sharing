from locationsharinglib import Service
from unidecode import unidecode

import sys
import time
import pyais
import extract_cookies
import latlon

data = {
    'mmsi': '30000000',
    'type': 19,
}


cookies_file = 'cookies.txt'
extract_cookies.extract_cookies(cookies_file)

google_email = 'land.rover.discoveryii2002@gmail.com'
#  google_email = 'emilia.partyka@gmail.com'

people = {}

while True:
    service = Service(cookies_file=cookies_file, authenticating_account=google_email)
    i=100000
    for person in service.get_all_people():
        #  print(person.nickname)
        #  print(person.latitude)
        
        data['lat']=person.latitude
        data['lon']=person.longitude
        data['shipname']=unidecode(person.nickname)
        data['mmsi']=str(i)
        #  print(person.datetime)
        #  print(person.timestamp)
        if person.nickname in people:
            A=latlon.LatLon(people[person.nickname][0], people[person.nickname][1])
            B=latlon.LatLon(person.latitude, person.longitude)
            distance_km=A.distance(B)
            distance_nm=distance_km/1.852
            time_in_hours=(person.timestamp-people[person.nickname][2])/1000/60/60
            #  print("A:", A)
            #  print("B:", B)
            #  print("distance_km", distance_km)
            #  print("distance_nm", distance_nm)
            #  print("time_in_hours", time_in_hours)
            if time_in_hours!=0:
                heading=round(A.heading_initial(B), 2)%360
                speed=round(distance_nm/time_in_hours, 2)
                #  print("speed", speed)
                data['speed']=str(speed)
                #  print("heading", heading)
                data['heading']=int(heading)
                data['course']=str(heading)
        people[person.nickname]=(person.latitude, person.longitude, person.timestamp)
        i+=1
        encoded = pyais.encode_dict(data, radio_channel="B", talker_id="AIVDM")
        print(encoded[0])
        sys.stdout.flush() 
        #nc -u 0.0.0.0 1234
    time.sleep(120)
