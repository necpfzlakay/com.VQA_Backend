import pyodbc 
import json
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=.;'
                      'Database=VQA;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

#
#





print("DATABASE CONNECTION SUCCESS")


def Login(username="",password=""):
    query = ""
    query = "SELECT Username,Email,Password FROM Login WHERE Username='"+username+"' AND Password = '"+password+"'"
    print("\nQuery: ",query)
    cursor.execute(query)
    usr = ""
    for i in cursor:
        usr = i
        print("USER LOGIN İNDEX İ -->",i)
        break
    if(usr == ""):
        return "false"
    return str(usr)

def Register(user_name="",email="",password=""):
    query = "INSERT INTO Login(Username,Email,Password) VALUES('"+user_name+"','"+email+"','"+password+"');"
    print("---------",query) 
    cursor.execute(query)
    cursor.commit()
    usr = "SELECT Username,Email,Password FROM Login WHERE Username='"+user_name+"' AND Password = '"+password+"'"
    cursor.execute(usr)
    usr = ""
    for i in cursor:
        usr = i
        print("indexxxxx",i)
        break
    if(usr == ""):
        return "false"
    return str(usr)
 

#    cursor.execute(query.format("username"=username,"email"=email,"password"=password))
 
