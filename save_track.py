import datetime

def save(name, lat, lon, timestamp):
    file_name = "tracks/"+name+".txt"
    time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    print("Save", name, lat, lon, time)
    with open(file_name, "a") as file:
        file.write('    <trkpt lat="'+str(lat)+'" lon="'+str(lon)+'">\n')
        file.write('      <time>')
        file.write(time)
        file.write('</time>\n')
        file.write('    </trkpt>\n')
