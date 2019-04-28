from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
from flask_cors import CORS
import re
import base64
#import jsonify


app = Flask(__name__)
CORS(app)
#CORS(app,resources={r"/*":{"origins":"*"}})
#app.config['JSON_SORT_KEYS'] = False
#app.config["CORS_SUPPORT_CREDENTIALS"] = True

def is_sha1(maybe_sha):
	if len(maybe_sha) != 40:
		return False
	try:
		sha_int = int(maybe_sha, 16)
	except ValueError:
		return False
	return True

def isBase64(s):
	try:
		return base64.b64encode(base64.b64decode(s)) == s
	except Exception:
		return False

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

def check_new_user(username):
	conn=sql.connect("assign.db")
	command = "SELECT * FROM user WHERE user_name='"+str(username)+"';"
	l = list(conn.execute(command))
	conn.commit()
	if(len(l)==0):
		#new user
		return 1
	else:
		#old user
		return 0

def update_counter():
	conn=sql.connect("assign.db")
	command = "SELECT count from count;"
	l = list(conn.execute(command))
	conn.commit()
	current_count = int(l[0][0])
	updated_count = current_count + 1

	command = "DELETE FROM count;"
	conn.execute(command)
	conn.commit()

	command = "INSERT INTO count VALUES('"+str(updated_count)+"');"
	conn.execute(command)
	conn.commit()

def reset_counter():
	conn=sql.connect("assign.db")
	
	updated_count = 0

	command = "DELETE FROM count;"
	conn.execute(command)
	conn.commit()

	command = "INSERT INTO count VALUES('"+str(updated_count)+"');"
	conn.execute(command)
	conn.commit()


@app.route('/')
def home():
	return jsonify({}),200

#api 1
@app.route('/api/v1/users',methods=["POST","GET","DELETE","PUT"])
def api_add_user():
	global count
	count += 1
	if request.method == 'POST':
		#print("Hello")
		userDataInJsonFormat = (request.get_json(force=True))
		print(userDataInJsonFormat)
		user_name = userDataInJsonFormat['username']
		user_type = check_new_user(user_name)
		if(user_type==0):
			return jsonify({}),400
		password = userDataInJsonFormat['password']
		#enc_password = hashlib.sha1(password.encode()) 
		#password = enc_password.hexdigest()
		if(is_sha1(password)==False):
			return jsonify({}),400   
		details = [user_name,password]
		print(details)
		add_user(details)

		return jsonify({}),201

	elif request.method == 'GET':
		conn=sql.connect("assign.db")
		command = "SELECT user_name FROM user;"
		l = list(conn.execute(command))
		conn.commit()
		print(l)
		if(len(l)==0):
			return jsonify({}),204
		#print(l)
		l = [i[0] for i in l]
		return jsonify(l),200

	elif request.method!='POST' and request.method!='GET':
		return jsonify({}),405
	#return render_template('test.html')
		


#api 2
@app.route('/api/v1/users/<username>',methods=["POST","GET","DELETE","PUT"])
def api_delete_user(username):
	global count
	count += 1
	if request.method == 'DELETE':
		#userDataInJsonFormat = (request.get_json())
		#print(userDataInJsonFormat)
		#user_name = userDataInJsonFormat['username']
		print(username)
		user_type = check_new_user(username)
		if user_type==1:
			#user name does not exist in the database
			return jsonify({}),400
		remove_user(str(username))

		return jsonify({}),200

	elif request.method!='DELETE':
		return jsonify({}),405

	return render_template('test.html')

@app.route('/api/v1/_count',methods=["POST","GET","DELETE","PUT"])
def api_counter():
	global count
	conn=sql.connect("assign.db")
	if request.method == 'GET':
		#command = "SELECT count from count;"
		#l = list(conn.execute(command))
		#conn.commit()
		#print(l[0][0])        
		return jsonify([count]),200

	elif request.method == 'DELETE':
		count = 0

		return jsonify({}),200

	else:
		return jsonify({}),405


if __name__ == '__main__':
	count = 0
	app.run(debug=True,host='0.0.0.0')    





