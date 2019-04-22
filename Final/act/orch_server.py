from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
from flask_cors import CORS
import re
import base64
import json
import time

app = Flask(__name__)
CORS(app)


@app.route('/<path:path>', methods=["POST","GET","DELETE","PUT"])
def orchestrator(path):
	global container_i
	which_container = container_i
	container_i = (container_i+1)%3
	#url = path.replace(':80/',':'+str(8000+which_container)+"/")
	url = "http://localhost:" + str(8000+which_container)+"/" +path
	print(url)
	if request.method == "GET":
		time.sleep(1)
		r = requests.get(url).status_code
		return jsonify({}),r
	elif request.method == "POST":
		time.sleep(1)
		#url = path.replace(':80/',':'+str(8000+which_container)+"/")
		r = requests.post(url, data = request.get_json(force=True)).status_code
		return jsonify({}),r
	elif request.method == "DELETE":
		time.sleep(1)
		#url = path.replace(':80/',':'+str(8000+which_container)+"/")
		r = requests.delete(url).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405




'''
#api 3 and 4
@app.route('/api/v1/categories', methods=["POST","GET","DELETE","PUT"])
def api_list_all_categories():
	print("In here ...")
	global container_i
	global urls
	if request.method == 'GET':
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/categories"
		r = requests.get(url_redirect).status_code
		return jsonify({}),r
	elif request.method == "POST":
		userDataInJsonFormat = request.get_json()
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/categories"
		r = requests.post(url_redirect,data = userDataInJsonFormat).status_code
		return josnify({}),r
	else:
		return jsonify({}),405

#api 5
@app.route('/api/v1/categories/<categoryName>' , methods=["POST","GET","DELETE","PUT"])
def api_remove_category(categoryName):
	global container_i
	global urls
	if request.method == 'DELETE':
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/categories/"+categoryName
		r = requests.delete(url_redirect).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405


#api 6 and api 8
@app.route('/api/v1/categories/<categoryName>/acts', methods=["POST","GET","DELETE","PUT"])
def api_list_acts_of_category(categoryName):
	global container_i
	global urls
	if request.method == 'GET':
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/categories/"+categoryName+"/acts"
		start = request.args.get('start',type = int,default=-1)
		end = request.args.get('end',type = int,default=-1)

		if(start==-1 and end==-1):
			r = requests.get(url_redirect).status_code
		
		else:
			url_redirect = url_redirect + "?start="+str(start)+"&end="+str(end)
			r = requests.get(url_redirect).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405


#api 7
@app.route('/api/v1/categories/<categoryName>/acts/size', methods=["POST","GET","DELETE","PUT"])
def api_number_of_act_in_a_category(categoryName):
	global container_i
	global urls
	if request.method == 'GET':
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/categories/"+categoryName+"/acts/size"
		r = requests.get(url_redirect).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405


#api 9
@app.route('/api/v1/acts/upvote' , methods=["POST","GET","DELETE","PUT"])
def api_upvote():
	global container_i
	global urls
	if request.method == 'POST':
		userDataInJsonFormat = request.get_json(force=True)
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/acts/upvote"
		r = requests.post(url_redirect,data = userDataInJsonFormat).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405

#api 10
@app.route('/api/v1/acts/<int:actID>' , methods=["POST","GET","DELETE","PUT"])
def api_remove_act(actID):
	global container_i
	global urls
	if request.method == 'DELETE':
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/acts/"+str(actID)
		r = requests.delete(url_redirect).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405

#api 11
@app.route('/api/v1/acts' , methods=["POST","GET","DELETE","PUT"])
def api_upload_act():
	global container_i
	global urls
	if requests.method == "POST":
		userDataInJsonFormat = (request.get_json(force=True))
		which_container = container_i
		container_i = (container_i+1)%3
		url_redirect = urls[which_container] + "/api/v1/acts"
		r = requests.post(url_redirect,data = userDataInJsonFormat).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405
'''

if __name__ == '__main__':
	urls = ["http://localhost:8000","http://localhost:8001","http://localhost:8002"]
	container_i = 0
	app.run(debug=True,host='0.0.0.0')