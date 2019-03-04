from flask import Flask,render_template ,redirect, url_for , request, jsonify
import requests
import sqlite3 as sql
import hashlib


app = Flask(__name__)
@app.route('/')
def login():
    return render_template("test.html")



if __name__ == '__main__':
    app.run(debug=True,port = 5002)
