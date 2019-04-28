from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib
from flask_cors import CORS
import re
import base64
import json
import time
import docker
import os
import signal
import subprocess
from threading import Thread
import threading

app = Flask(__name__)
CORS(app)


@app.route('/<path:path>', methods=["POST","GET","DELETE","PUT"])
def orchestrator(path):
	global container_i
	global request_count
	global active_containers

	if ((path != '/api/v1/_health') or (path != '/api/v1/_crash')):
		request_count+=1

	which_container = get_next_container(active_containers)
	#container_i = (container_i+1)%container_count
	#url = path.replace(':80/',':'+str(8000+which_container)+"/")
	url = "http://localhost:" + str(8000+which_container)+"/" +path
	print(url)
	#return redirect(url)
	if request.method == "GET":
		#time.sleep(1)
		r = requests.get(url).status_code
		return jsonify({}),r
	elif request.method == "POST":
		#time.sleep(1)
		#url = path.replace(':80/',':'+str(8000+which_container)+"/")
		try:
			r = requests.post(url, data = request.get_json(force=True)).status_code
		except:
			r = requests.post(url, data = None).status_code
		return jsonify({}),r
	elif request.method == "DELETE":
		#time.sleep(1)
		#url = path.replace(':80/',':'+str(8000+which_container)+"/")
		r = requests.delete(url).status_code
		return jsonify({}),r
	else:
		return jsonify({}),405

def get_next_container(active_containers):
	global container_i
	container_i = (container_i+1)%len(active_containers)
	return container_i


sem = threading.Semaphore()
def fun2():
	sem.acquire()
	
	i = 1
	while True:
		time.sleep(1)
		print("health check batch : ", i)
		global active_containers
		i += 1
		for cont in active_containers:
			print(cont)
			time.sleep(1)
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
			if requests.get("http://localhost:"+str(cont['port'])+"/api/v1/_health", headers=headers).status_code != 200:
				stop_container(cont['port'])
				time.sleep(1)
				run_container(cont['port'])
			
	sem.release()




def stop_container(port_no):
	sem.acquire()
	print("Stopping on port :",port_no)
	global container_count
	global active_containers
	#time.sleep(1)
	#cont_dict = active_containers[container_count-1]
	cont_dict = [i for i in active_containers if i['port']==port_no][0]
	#stop_cmd = "sudo docker container stop "+cont_dict['name']
	#subprocess.call(stop_cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	#remove_cmd = "sudo docker container remove "+cont_dict['name']
	#subprocess.call(remove_cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	kill_cmd = "docker rm -f "+cont_dict['id']
	subprocess.call(kill_cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	container_count-=1
	active_containers.remove(cont_dict)
	print("stopping container ",cont_dict['name'])
	sem.release()


def run_container(port_no):
	#sem.acquire()
	print('Starting on port :',port_no)
	global container_count
	global active_containers
	run_cmd = "sudo docker run -d -p "+str(port_no)+":5000 -it acts --name acts"+str(port_no)
	container_count+=1
	pro = subprocess.call(run_cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	
	output = subprocess.check_output(['docker','ps'])#, stdout=subprocess.PIPE)
	l = output.split('\n')
	print([l[i][:12] for i in range(1,len(l))])
	container_id = l[1][:12]
	k = {'name':"acts"+str(port_no),'port':port_no,'id':container_id}
	active_containers.append(k)
	#print(type(output))
	#sem.release()

def start():
	sem.acquire()
	global app
	#app.debug=True
	run_container(8000)
	sem.release()
	#app.run(host='0.0.0.0', port=80)
	app.run(debug=False,host='0.0.0.0',port = 80,threaded=True)


def get_active_ports(active_containers):
	l = []
	for i in active_containers:
		l.append(i['port'])
	return l


def fun3():
	global active_containers
	global request_count
	size = len(active_containers)
	while True:
		time.sleep(20)
		while len(active_containers) > int(request_count / 5)+1:
			active_ports = get_active_ports(active_containers)
			stop_container(active_ports[-1])
		while len(active_containers) < int(request_count / 5)+1:
			run_container(len(active_containers)+8000)
		request_count = 0


if __name__ == '__main__':

	#request count - auto scaling
	request_count = 0
	container_count = 0
	#which container to forward the request
	container_i = -1

	#list of active containers
	active_containers = []
	#for i in range(8000,8006):
	#	run_container(i)
		
	
	#for i in range(8000,8003):
	#	stop_container(i)
	thread1 = threading.Thread(target = start)
	thread1.start()
	thread2 = threading.Thread(target = fun2)
	time.sleep(5)
	thread2.start()
	thread3 = threading.Thread(target = fun3)
	time.sleep(5)
	thread3.start()
