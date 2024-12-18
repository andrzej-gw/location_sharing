import argparse
import extract_cookies
import latlon
import locationsharinglib
import multiprocessing
import pyais
import socket
import sys
import time
import unidecode



def get_nmea_data(file, cond):
    google_email = 'land.rover.discoveryii2002@gmail.com'

    people = {}

    data={}

    while True:
        service = locationsharinglib.Service(cookies_file=cookies_file, authenticating_account=google_email)
        i=100000
        for person in service.get_all_people():
            if not person.nickname in data:
                data[person.nickname]={
                    'mmsi': '30000000',
                    'type': 19,
                }
            data[person.nickname]['lat']=person.latitude
            data[person.nickname]['lon']=person.longitude
            data[person.nickname]['shipname']=unidecode.unidecode(person.nickname)
            data[person.nickname]['mmsi']=str(i)
            if person.nickname in people:
                A=latlon.LatLon(people[person.nickname][0], people[person.nickname][1])
                B=latlon.LatLon(person.latitude, person.longitude)
                distance_km=A.distance(B)
                distance_nm=distance_km/1.852
                time_in_hours=(person.timestamp-people[person.nickname][2])/1000/60/60
                if time_in_hours!=0:
                    heading=round(A.heading_initial(B), 2)%360
                    speed=round(distance_nm/time_in_hours, 2)
                    data[person.nickname]['speed']=str(speed)
                    data[person.nickname]['heading']=int(heading)
                    data[person.nickname]['course']=str(heading)
            people[person.nickname]=(person.latitude, person.longitude, person.timestamp)
            i+=1
            encoded = pyais.encode_dict(data[person.nickname], radio_channel="B", talker_id="AIVDM")
            file.write(encoded[0]+"\n")
            file.flush()
            with cond:
                cond.notify_all()
            #  print(encoded[0])
            #  sys.stdout.flush() 
            #nc -u 0.0.0.0 1234
        time.sleep(120)

def handle_client(client_socket):
    try:
        file = open("nmea_data", "r")
        lines = file.read()
        lines = lines[max(0,len(lines)-72*10):] # Read last 10 messsages
        client_socket.sendall(lines.encode('utf-8'))
        print(f"Sent NMEA data to client: {lines}")
        while True:
            lines=file.read()
            with cond:
                while not lines:
                    cond.wait()
                    lines=file.read()
                    
                # Send NMEA to the client
                client_socket.sendall(lines.encode('utf-8'))
                print(f"Sent NMEA data to client: {lines}")
    except Exception as e:
        print(f"Error with client: {e}")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=49903):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Listen for incoming connections
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = multiprocessing.Process(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Shutting down the server...")
    finally:
        server_socket.close()
        print("Server socket closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cookies_file', help=
    'you can pass your cookies file or it will be loaded from your browser')
    parser.add_argument('--port', help=
    'you can pass port number or it will be 49903')
    args = parser.parse_args()

    if args.cookies_file==None:
        cookies_file = 'cookies.txt'
        extract_cookies.extract_cookies(cookies_file)
    else:
        cookies_file=args.cookies_file
        
    if args.port==None:
        port = 49903
    else:
        port=int(args.port)


    file = open("nmea_data", "w")
    
    cond = multiprocessing.Condition()

    nmea_getter = multiprocessing.Process(target=get_nmea_data, args=(file,cond))
    nmea_getter.start()

    start_server(port=port)
