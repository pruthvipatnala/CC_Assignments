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

def add_category(categoryName):
    conn=sql.connect("assign.db")
    command = "INSERT INTO category(category_name,act_count) values ('"+str(categoryName)+"','"+str(0)+"');"
    conn.execute(command)
    conn.commit()

def get_act_counts():
    conn=sql.connect("assign.db")
    command = "select * from category"
    l = list(conn.execute(command))
    #print(l)
    act_count_dict  = dict()
    for i in l:
        act_count_dict[i[0]] = int(i[1])

    return act_count_dict

def remove_category(categoryName):
    conn=sql.connect("assign.db")
    command = "DELETE FROM category WHERE category_name='"+str(categoryName)+"';"
    conn.execute(command)
    conn.commit()


#api 1
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
        
#api 2
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

#api 3
@app.route('/api/v1/categories', methods=["POST","GET","DELETE","PUT"])
def api_list_all_categories():
    if request.method == 'GET':
        #userDataInJsonFormat = (request.get_json())
        act_count_dict = get_act_counts()

        return jsonify(act_count_dict),200



#api 4
@app.route('/api/v1/categories', methods=["POST","GET","DELETE","PUT"])
def api_add_category():
    if request.method == 'POST':
        userDataInJsonFormat = (request.get_json())
        for i in userDataInJsonFormat:
            add_category(i)

        return jsonify({}),200


#api 5
@app.route('/api/v1/categories/<categoryName>' , methods=["POST","GET","DELETE","PUT"])
def api_remove_category(categoryName):
    if request.method == 'DELETE':
        remove_category(categoryName)

        return jsonify({}),200




if __name__ == '__main__':
    app.run(debug=True,port = 5001)
