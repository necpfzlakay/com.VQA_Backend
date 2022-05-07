import json
import pymssql

conn = pymssql.connect(server='.', database='VQA')
#conn = pymssql.connect(server='.', user='yourusername@yourserver', password='yourpassword', database='AdventureWorks')

cursor = conn.cursor() 
print(cursor)

def history(username=""):
    if (username == ""):
        return False
    usr = str(username)
    cursor.execute("SELECT * FROM history WHERE username= '"+usr+"'" )
    row = cursor.fetchall()
    
    print(json.dumps(row))

    return json.dumps(row)


def addHistory(username, question,answer, photoName):
    print()
    
    query = "insert into History values('"+username+"','"+question+"','"+answer+"', '"+photoName+"')"
    
    try:
        cursor.execute(query)
        cursor.commit()
        return True
    except:
        return False


