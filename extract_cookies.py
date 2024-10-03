import sqlite3 

import os


def extract_cookies(file_name):  
    # Connecting to sqlite 
    # connection object
    
    os.system('cp ~/snap/firefox/common/.mozilla/firefox/m52ljqqk.default/cookies.sqlite cookies.sqlite')
    
    connection_obj = sqlite3.connect('cookies.sqlite') 
      
    # cursor object 
    cursor_obj = connection_obj.cursor() 
      
    # to select all column we will use 
    #  statement = '''SELECT * FROM moz_cookies'''
    statement = '''select host,
        case substr(host,1,1)='.' when 0 then 'FALSE' else 'TRUE' end,
        path,
        case isSecure when 0 then 'FALSE' else 'TRUE' end,
        expiry,
        name,
        value
        from moz_cookies
        WHERE host='.google.com';'''
    #  statement = '''select domain, flag, path, secure, expiry, name, value
        #  from moz_cookies;'''
      
    cursor_obj.execute(statement) 
      
    output = cursor_obj.fetchall()
    
    file = open(file_name, "w")
    
    for row in output:
        for element in row: 
            file.write(str(element)+"\t")
        file.write("\n")
    file.close()
      
    connection_obj.commit() 
      
    # Close the connection 
    connection_obj.close()
    os.system('rm cookies.sqlite')
