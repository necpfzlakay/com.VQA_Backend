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
    print(f'adding to database history {username} {question} {answer} {photoName}')
    
    query = "insert into History values('"+username+"','"+question+"','"+answer+"','"+photoName+"')"
    print(query)
    try:
        cursor.execute(query)
        conn.commit()
        print(True)
        return True
    except:
        print(False)
        return False


# addHistory("userngggame", "quggggestion", "angggswer", "ggggg")

