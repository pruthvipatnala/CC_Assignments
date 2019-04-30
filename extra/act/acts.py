
from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
from flask_cors import CORS
import re
import base64
import json




url="http://54.92.213.23:80/api/v1/users"
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
	return "hello world" 


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
	#delete from category table
	command = "DELETE FROM category WHERE category_name='"+str(categoryName)+"';"
	conn.execute(command)
	conn.commit()
	#delete from act table (cascade effect)
	command = "DELETE FROM act WHERE category_name='"+str(categoryName)+"';"
	conn.execute(command)
	conn.commit()


def check_new_user(username):
	if(username not in json.loads(requests.get(url).text)):
		#new user
		return 1
	else:
		#old user
		return 0

def check_new_category(categoryName):
	conn=sql.connect("assign.db")
	command = "SELECT * FROM category WHERE category_name='"+str(categoryName)+"';"
	l = list(conn.execute(command))
	conn.commit()
	#print("Before l")
	print(l)
	#print("after l")
	if(len(l)==0):
		#new category
		return 1
	else:
		#old category
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


#api 3 and 4
@app.route('/api/v1/categories', methods=["POST","GET","DELETE","PUT"])
def api_list_all_categories():
	global count
	count += 1
	if request.method == 'GET':
		#userDataInJsonFormat = (request.get_json())
		#print(userDataInJsonFormat)
		
		#if(userDataInJsonFormat!={}):
		#	return jsonify({}),400
		
		act_count_dict = get_act_counts()

		return jsonify(act_count_dict),200

	elif request.method == 'POST':
		userDataInJsonFormat = (request.get_json())
		print(type(userDataInJsonFormat))
		for i in userDataInJsonFormat:
			if(check_new_category(i)==0):
				return jsonify({}),400
			add_category(i)

		return jsonify({}),201

	elif request.method!='GET' and request.method!='POST':
		return jsonify({}),405


'''
#api 4
@app.route('/api/v1/categories', methods=["POST","GET","DELETE","PUT"])
def api_add_category():
	if request.method == 'POST':
		userDataInJsonFormat = (request.get_json())
		for i in userDataInJsonFormat:
			if(check_new_category(i)==0):
				return jsonify({}),400
			add_category(i)
		return jsonify({}),201
	elif request.method!='POST':
		return jsonify({}),405
'''


#api 5
@app.route('/api/v1/categories/<categoryName>' , methods=["POST","GET","DELETE","PUT"])
def api_remove_category(categoryName):
	global count
	count += 1
	if request.method == 'DELETE':
		if check_new_category(categoryName)==1:
			return jsonify({}),400

		remove_category(categoryName)
		return jsonify({}),200

	elif request.method != 'DELETE':
		return jsonify({}),405



#api 6 and api 8

#note : need to handle status code 204

@app.route('/api/v1/categories/<categoryName>/acts', methods=["POST","GET","DELETE","PUT"])
def api_list_acts_of_category(categoryName):
	global count
	count += 1
	if request.method == 'GET':
		conn=sql.connect("assign.db")
		command = "SELECT * FROM act WHERE category_name= '"+str(categoryName)+"';"
		l = list(conn.execute(command))
		conn.commit()
		if(len(l)==0 and check_new_category(categoryName)==0):
			return jsonify({}),204


		#print(l)
		start = request.args.get('start',type = int,default=-1)
		end = request.args.get('end',type = int,default=-1)
		#print(start,end)

		if(start==-1 and end==-1):
			output = []
			server_limit = 99
			request_length = len(l)

			if(request_length>server_limit):
				return jsonify({}),413

			for i in l:
				#print(i)
				d = {'actId':i[1],"username":i[2],'timestamp':i[3],'caption':i[4],'upvotes':i[5],'imgB64':i[6]}
				output.append(d)

			#print(output)
			return jsonify(output),200

		elif(start!=-1 and end!=-1):
			if(not(start>0 and end <=len(l) and start<=end)):
				return jsonify({}),400

			output = []
			for i in l[start-1:end]:
				d = {'actId':i[1],"username":i[2],'timestamp':i[3],'caption':i[4],'upvotes':i[5],'imgB64':i[6]}
				output.append(d)

			return jsonify(output),200

		else:
			return jsonify({}),400

		

	elif request.method != 'GET':
		return jsonify({}),405        


#api 7
@app.route('/api/v1/categories/<categoryName>/acts/size', methods=["POST","GET","DELETE","PUT"])
def api_number_of_act_in_a_category(categoryName):
	global count
	count += 1
	if request.method=="GET":
		conn=sql.connect("assign.db")
		command = "SELECT * FROM category WHERE category_name= '"+str(categoryName)+"';"
		l = list(conn.execute(command))
		conn.commit()
		#print(l)
		if(len(l)==0):
			return jsonify({}),400


		command = "SELECT COUNT(*) FROM act WHERE category_name= '"+str(categoryName)+"';"
		l = list(conn.execute(command))
		conn.commit()
		count = l[0][0]


		return jsonify([count]),200

	elif request.method != 'GET':
		return jsonify({}),405


#api 9
@app.route('/api/v1/acts/upvote' , methods=["POST","GET","DELETE","PUT"])
def api_upvote():
	global count
	count += 1
	if request.method=='POST':
		userDataInJsonFormat = request.get_json(force=True)
		actID = str(userDataInJsonFormat[0])
		#print(actID)
		conn = sql.connect("assign.db")
		command = "SELECT * from act WHERE actID ='"+actID+"';"
		try:
			current_count = int(list(conn.execute(command))[0][5])
			conn.commit()
		except:
			return jsonify({}),400
		command = "UPDATE act SET upvotes='"+str(current_count+1)+"' WHERE actID='"+actID+"';"
		conn.execute(command)
		conn.commit()

		return jsonify({}),200
	elif request.method != 'POST':
		return jsonify({}),405


#api 10
@app.route('/api/v1/acts/<int:actID>' , methods=["POST","GET","DELETE","PUT"])
def api_remove_act(actID):
	global count
	count += 1
	if request.method== "DELETE":

		conn = sql.connect('assign.db')
		#get category name
		command = "SELECT category_name FROM act WHERE actID = '"+str(actID)+"';"
		try:
			category_name = list(conn.execute(command))[0][0]
			conn.commit()
			print(category_name)
		except:
			#print('sup')
			return jsonify({}),400

		command = "DELETE FROM act WHERE actID = '"+str(actID)+"';"
		conn.execute(command)
		conn.commit()

		#update category table
		command = "SELECT act_count from category where category_name = '"+str(category_name)+"';"
		current_count = int(list(conn.execute(command))[0][0])
		conn.commit()

		command = "UPDATE category SET act_count='"+str(current_count-1)+"' WHERE category_name='"+str(category_name)+"';"
		conn.execute(command)
		conn.commit()

		return jsonify({}),200

	elif request.method != 'DELETE':
		return jsonify({}),405



#api 11
@app.route('/api/v1/acts' , methods=["POST","GET","DELETE","PUT"])
def api_upload_act():
	global count
	count += 1
	if request.method=='POST':
		userDataInJsonFormat = (request.get_json(force=True))
		actID = userDataInJsonFormat['actId']
		username = userDataInJsonFormat['username']
		timestamp = userDataInJsonFormat['timestamp']
		pattern = re.compile("\d+-\d+-\d\d\d\d:\d+-\d+-\d+")
		if(pattern.match(timestamp)==None):
			print("Invalid timestamp")
			return jsonify({}),400

		caption = userDataInJsonFormat['caption']
		categoryName = userDataInJsonFormat['categoryName']
		imgB64 = userDataInJsonFormat['imgB64']
		imgB64_byte = imgB64.encode('utf-8')
		if(isBase64(imgB64_byte)==False):
			print("Failed because of image base64 issue")
			return jsonify({}),400

		if not username in json.loads(requests.get("http://54.92.213.23/api/v1/users").text):
			print("invalid user")
			return jsonify({}),400
		try:
			upvotes = userDataInJsonFormat['upvotes']
			print(upvotes)
			return jsonify({}),400

		except:
			upvotes = 0
			#The username must exist, otherwise send the appropriate response code from the given list.
			if(check_new_user(username)==1):
				print("Yes new user")
				return jsonify({}),400

			conn = sql.connect('assign.db')

			if(check_new_category(categoryName)==1):
				print("Uploading an act for an unknown category")
				return jsonify({}),400                

			try :
				command = "INSERT INTO act values ('"+str(categoryName)+"','"+str(actID)+"','"+str(username)+"','"+str(timestamp)+"','"+str(caption)+"','"+str(upvotes)+"','"+str(imgB64)+"');"
				#print(command)
				conn.execute(command)
				conn.commit()

			except:
				print("in here 1")
				return jsonify({}),400

			try:
				command = "SELECT act_count from category where category_name = '"+str(categoryName)+"';"
				current_count = int(list(conn.execute(command))[0][0])
				conn.commit()
			except:
				print("in here 2")
				return jsonify({}),400

			try:
				command = "UPDATE category SET act_count='"+str(current_count+1)+"' WHERE category_name='"+str(categoryName)+"';"
				conn.execute(command)
				conn.commit()

				return jsonify({}),201
			except:
				print("in here 3")
				return jsonify({}),400

	elif request.method != 'POST':
		return jsonify({}),405

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


#health checking api
@app.route('/api/v1/_health',methods = ["POST","GET","DELETE","PUT"])
def health_checker():
	if request.method == "GET":
		global crash_status
		if(crash_status==1):
			return jsonify({}),500

		print("In health checker")
		stat_codes = []
		#api 1 check - create user
		data = {"username":"test_user","password":"3d725109c7e7c0bfb9d709836735b56d943d263f"}
		r = requests.post('http://54.92.213.23:80/api/v1/users',data = json.dumps(data))
		print("Status code after user creation = ",r.status_code)
		#print(r.json())
		stat_codes.append(r.status_code)

		#r = requests.get('http://localhost:5000/api/v1/_count').status_code
		#stat_codes.append(r)
		#api 3 check
		print("API 3")
		r = requests.get('http://localhost:5000/api/v1/categories',data = "{}").status_code
		stat_codes.append(r)
		#api 4 check - create a category
		print("API 4")
		r = requests.post('http://localhost:5000/api/v1/categories',json = ["test_category"]).status_code
		stat_codes.append(r)
		#api 11 check upload act
		print("API 11")
		data = {"actId": 1234,"username": "test_user","timestamp": "10-12-2018:59-59-3","caption": "caption text","categoryName": "test_category","imgB64":"c2FkYXNkYXNjYXNjYXNkY2FrZHNmY2FzbmMsYXNjIGFza2Nha2Msc20gYyxhcyBjYXNuYy5hbHNrY25hc2w="}
		r = requests.post('http://localhost:5000/api/v1/acts',json = data).status_code
		stat_codes.append(r)
		#api 9 check upvote uploaded act
		print("API 9")
		r = requests.post('http://localhost:5000/api/v1/acts/upvote',json = [1234]).status_code
		stat_codes.append(r)
		#api 7 check - number of acts in test_category
		print("API 7")
		r = requests.get('http://localhost:5000/api/v1/categories/test_category/acts/size').status_code
		stat_codes.append(r)
		#api 6 check - list the acts in test_category
		print("API 6")
		r = requests.get('http://localhost:5000/api/v1/categories/test_category/acts').status_code
		stat_codes.append(r)
		#api 8 check - number of acts in a given range
		print("API 8")
		r = requests.get('http://localhost:5000/api/v1/categories/test_category/acts?start=1&end=1').status_code
		stat_codes.append(r)
		#api 10 check - remove act
		print("API 10")
		r = requests.delete('http://localhost:5000/api/v1/acts/1234').status_code
		stat_codes.append(r)
		#api 5 check - remove category
		print("API 5")
		r = requests.delete('http://localhost:5000/api/v1/categories/test_category').status_code
		stat_codes.append(r)

		#api 2 check - delete user
		print("API 2")
		r = requests.delete('http://54.92.213.23:80/api/v1/users/test_user').status_code
		stat_codes.append(r)


		print(stat_codes)

		for i in stat_codes:
			if i//100!=2:
				return jsonify({}),500
		return jsonify({}),200
	else:
		return jsonify({}),405

#server crash api
@app.route('/api/v1/_crash',methods = ["POST","GET","DELETE","PUT"])
def server_crash():
	if request.method == 'POST':
		global crash_status
		crash_status = 1
		return jsonify({}),200

	else:
		return jsonify({}),405


@app.route('/_keepbusy',methods = ["POST","GET","DELETE","PUT"])
def keep_busy():
	global busy
	busy = 1
	return jsonify({}),200

@app.route('/_keepfree',methods = ["POST","GET","DELETE","PUT"])
def keep_free():
	global busy
	busy = 0
	return jsonify({}),200

@app.route('/_isbusy',methods = ["POST","GET","DELETE","PUT"])
def isbusy():
	global busy
	if(busy==1):
		return jsonify({}),200
	else:
		return jsonify({}),500



if __name__ == '__main__':
	busy = 0
	count = 0
	crash_status = 0
	app.run(debug=True,host='0.0.0.0')


