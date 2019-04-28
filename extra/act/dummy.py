from flask import Flask, render_template, request, redirect, abort
import threading
import requests
import time, signal, sys
import docker

apis =	['/api/v1/_count',
		'/api/v1/_health',
		'/api/v1/_crash',
		'/api/v1/categories',
		'/api/v1/categories/<categoryName>/acts/size',
		'/api/v1/categories/<categoryName>/acts',
		'/api/v1/categories/<categoryName>',  	
		'/api/v1/acts/count',
		'/api/v1/acts/upvote',
		'/api/v1/acts/<actId>',
		'/api/v1/acts']


app = Flask(__name__)

sem = threading.Semaphore()

class roundrobin(object):
	"""docstring for roundrobin"""
	def __init__(self):
		super(roundrobin, self).__init__()
		self.containers = []
		self.next = -1
		self.size = 0
		self.tot_reqs = 0
		self.client = docker.from_env()

	def getnext(self):
		self.next = (self.next + 1) % self.size
		return self.containers[self.next]["port"]

	def startnewcontainer(self, port, idx):
		cont = self.client.containers.run("acts", detach=True, ports={'5000/tcp': port})
		if idx < self.size:
			self.containers[idx] = {'id':cont.id, 'port':port}
		else:
			self.containers.append({'id':cont.id, 'port':port})
		print(self.client.containers.list())
		time.sleep(5)
		self.size += 1
		
	def stopcontainer(self, idx):
		self.client.containers.get(self.containers[idx]['id']).stop()
		self.size -= 1

	def __del__(self):
		print("\ndestroying containers")
		for ii, i in enumerate(self.containers):
			self.stopcontainer(ii)

r = roundrobin()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
	global r, apis
	path = '/' + path
	if (path not in apis) or r.size == 0:
		abort(404)
	if ((path != '/api/v1/_health') or (path != '/api/v1/_crash')):
		r.tot_reqs += 1
	port = r.getnext()
	print("http://35.173.133.243:"+str(port)+path)
	return redirect("http://35.173.133.243:"+str(port)+path)

def fun1():
	sem.acquire()
	global app, r
	app.debug=True
	r.startnewcontainer(8000, 0)
	sem.release()
	#app.run(host='0.0.0.0', port=80)
	app.run(debug=True,host='0.0.0.0',port = 80,threaded=True)

def fun2():
	sem.acquire()
	i = 1
	while True:
		time.sleep(1)
		print("health check batch : ", i)
		i += 1
		for c, cont in enumerate(r.containers):
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
			if requests.get("http://35.173.133.243:"+str(cont['port'])+"/api/v1/_health", headers=headers).status_code != 200:
				r.stopcontainer(c)
				r.startnewcontainer(cont['port'], c)
	sem.release()


def fun3():
	global r
	while true:
		time.sleep(120)
		while r.size > int(r.tot_reqs / 20)+1:
			stopcontainer(self.size-1)
		while r.size < int(r.tot_reqs / 20)+1:
			startnewcontainer(self.size+8000, self.size)
		r.tot_reqs = 0


def handler(sig, frame):
	global r
	r.__del__()
	sys.exit(0)


if  __name__ == "__main__":
	
	signal.signal(signal.SIGINT, handler)
	print('press CTRL+C to exit')
	

	thread1 = threading.Thread(target = fun1)
	#app.debug=True
	#r.startnewcontainer(8000, 0)
	#app.run(debug=True,host='0.0.0.0',port = 5000,threaded=True)
	#fun1()
	thread2 = threading.Thread(target = fun2)
	thread3 = threading.Thread(target = fun3)
	thread1.start()
	thread2.start()
	thread3.start()

