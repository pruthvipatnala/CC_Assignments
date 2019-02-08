from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
#import jsonify


app = Flask(__name__)
@app.route('/home')
def home():
    return render_template("homepage.html")

def add_user(details):
    #details = [user_id,user_name,contact_no,email_id,password]
    conn=sql.connect("assign.db")
    command = "INSERT INTO user(user_name,password) values ('"+str(details[0])+"','"+str(details[1])+"');"
    conn.execute(command)
    conn.commit()

def remove_user(user_name):
    conn=sql.connect("assign.db")
    command = "DELETE FROM user WHERE user_name='"+str(user_name)+"';"
    conn.execute(command)
    conn.commit()


@app.route('/api/v1/users',methods=["POST","GET","DELETE","PUT"])
def api_add_user():
    if request.method == 'POST':
        #conn=sql.connect("assign.db")
        #command = "select count(*) from user;"
        #n = int(list(conn.execute(command))[0][0])
        #conn.commit()
        #print(n)
        userDataInJsonFormat = (request.get_json())
        user_name = userDataInJsonFormat['username']
        password = userDataInJsonFormat['password']
        enc_password = hashlib.sha1(password.encode()) 
        password = enc_password.hexdigest()
        details = [user_name,password]
        print(details)
        add_user(details)
        
        return jsonify({}),200
        
        
    return render_template('test.html')
        

@app.route('/api/v1/users/<username>',methods=["POST","GET","DELETE","PUT"])
def api_delete_user(username):
    if request.method == 'DELETE':
        #userDataInJsonFormat = (request.get_json())
        #print(userDataInJsonFormat)
        #user_name = userDataInJsonFormat['username']
        print(username)
        remove_user(str(username))

        return jsonify({}),200

    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True,port = 5001)
