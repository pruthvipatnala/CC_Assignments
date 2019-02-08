from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
# /import jsonify


app = Flask(__name__)
@app.route('/home')
def home():
    return render_template("homepage.html")

def add_user(details):
    #details = [user_id,user_name,contact_no,email_id,password]
    conn=sql.connect("assign.db")
    command = "INSERT INTO user(user_id,user_name,contact_no,email_id,password) values ('"+str(details[0])+"','"+str(details[1])+"','"+str(details[2])+"','"+str(details[3])+"','"+str(details[4])+"');"
    conn.execute(command)
    conn.commit()


@app.route('/api/v1/users',methods=["POST","GET","DELETE","PUT"])
def api_add_user():
    if request.method == 'POST':
        conn=sql.connect("assign.db")
        command = "select count(*) from user;"
        n = int(list(conn.execute(command))[0][0])
        conn.commit()
        #print(n)
        userDataInJsonFormat = (request.get_json())
        user_id = userDataInJsonFormat['user_id']
        user_name = userDataInJsonFormat['username']
        contact_no = userDataInJsonFormat['contact_no']
        email_id = userDataInJsonFormat['email_id']
        password = userDataInJsonFormat['password']
        
        details = [user_id,user_name,contact_no,email_id,password]
        print(details)
        add_user(details)
        
        return jsonify({}),200
        
        
    return render_template('test.html')
        




if __name__ == '__main__':
    app.run(debug=True,port = 5001)
