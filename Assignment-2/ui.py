from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
#import jsonify
from collections import OrderedDict


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
        #print("Hello")
        userDataInJsonFormat = (request.get_json(force=True))
        print(userDataInJsonFormat)
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



#api 6 and api 8
@app.route('/api/v1/categories/<categoryName>/acts', methods=["POST","GET","DELETE","PUT"])
def api_list_acts_of_category(categoryName):
    if request.method == 'GET':
        conn=sql.connect("assign.db")
        command = "SELECT * FROM act WHERE category_name= '"+str(categoryName)+"';"
        l = list(conn.execute(command))
        #print(l)
        start = request.args.get('start',type = int,default=-1)
        end = request.args.get('end',type = int,default=-1)
        
        if(start==-1 or end==-1):
            output = []
            for i in l:
                d = {'actID':i[1],"username":i[2],'timestamp':i[3],'caption':i[4],'upvotes':i[5],'imgB64':i[6]}
                output.append(d)

            return jsonify(output),200

        elif(start!=-1 and end!=-1):
            output = []
            for i in l[start:end+1]:
                d = {'actID':i[1],"username":i[2],'timestamp':i[3],'caption':i[4],'upvotes':i[5],'imgB64':i[6]}
                output.append(d)

            return jsonify(output),200            


#api 7
@app.route('/api/v1/categories/<categoryName>/acts/size', methods=["POST","GET","DELETE","PUT"])
def api_number_of_act_in_a_category(categoryName):
    if request.method=="GET":
        conn=sql.connect("assign.db")
        command = "SELECT COUNT(*) FROM act WHERE category_name= '"+str(categoryName)+"';"
        count = list(conn.execute(command))[0][0]

        return jsonify([count]),200


#api 9
@app.route('/api/v1/acts/upvote' , methods=["POST","GET","DELETE","PUT"])
def api_upvote():
    if request.method=='POST':
        userDataInJsonFormat = request.get_json(force=True)
        actID = str(userDataInJsonFormat[0])
        #print(actID)
        conn = sql.connect("assign.db")
        command = "SELECT * from act WHERE actID ='"+actID+"';"
        current_count = int(list(conn.execute(command))[0][5])
        conn.commit()
        command = "UPDATE act SET upvotes='"+str(current_count+1)+"' WHERE actID='"+actID+"';"
        conn.execute(command)
        conn.commit()

        return jsonify({}),200





if __name__ == '__main__':
    app.run(debug=True,port = 5001)
