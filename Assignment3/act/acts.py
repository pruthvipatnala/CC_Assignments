from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
from flask_cors import CORS
import re
import base64
#import jsonify

url = "http://3.80.241.172:8080/api/v1/users"

app = Flask(__name__)
CORS(app)

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

def check_new_category(categoryName):
	conn=sql.connect("assign.db")
	command = "SELECT * FROM category WHERE category_name='"+str(categoryName)+"';"
	l = list(conn.execute(command))
	conn.commit()
	if(len(l)==0):
		#new category
		return 1
	else:
		#old category
		return 0


@app.route('/api/v1/categories', methods=["POST","GET","DELETE","PUT"])
def api_list_all_categories():
	if request.method == 'GET':
		userDataInJsonFormat = (request.get_json())
		print(userDataInJsonFormat)
		
		if(userDataInJsonFormat!={}):
			return jsonify({}),400
		
		act_count_dict = get_act_counts()

		return jsonify(act_count_dict),200

	elif request.method == 'POST':
		userDataInJsonFormat = (request.get_json())
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
	if request.method=='POST':
		userDataInJsonFormat = (request.get_json(force=True))
		actID = userDataInJsonFormat['actId']
		username = userDataInJsonFormat['username']
		timestamp = userDataInJsonFormat['timestamp']
		pattern = re.compile("\d+-\d+-\d\d\d\d:\d+-\d+-\d+")
		if(pattern.match(timestamp)==None):
			return jsonify({}),400

		caption = userDataInJsonFormat['caption']
		categoryName = userDataInJsonFormat['categoryName']
		imgB64 = userDataInJsonFormat['imgB64']
		imgB64_byte = imgB64.encode('utf-8')
		if(isBase64(imgB64_byte)==False):
			return jsonify({}),400

		try:
			if not username in json.loads(requests.get(url)):
				print("invalid user")
				return jsonify({}),400
		except Exception as e:
			print("connection error")
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



if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')

