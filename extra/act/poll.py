#from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import time

#app = Flask(__name__)
#CORS(app)


#@app.route('/_poll',methods=["POST","GET","DELETE","PUT"])
#def poll():

j=0
while(True):
	time.sleep(1)
	j+=1
	r = requests.get('http://34.201.108.94:80/_get_active_containers/'+str(j)).json()
	for i in list(r):
		if requests.get('http://34.201.108.94:'+str(i)+"/api/v1/_health").status_code != 200:
			r_delete = requests.get('http://34.201.108.94:80/_del_container/'+str(i)).status_code
			print("Status code for deleting container at ",i,"  = ",r_delete)
			r_create = requests.get('http://34.201.108.94:80/_run_container/'+str(i)).status_code
			print("Status code for creating container at ",i,"  = ",r_create)
	print(str(j)+" - "+str(r))



