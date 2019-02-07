from flask import Flask,render_template ,redirect, url_for , request
import requests
import sqlite3 as sql
import jsonify


app = Flask(__name__)
@app.route('/home')
def home():
    return render_template("homepage.html")

def add_user(details):
    #details = [user_id,user_name,contact_no,email_id,password]
    conn=sql.connect("assign.db")
    command = "INSERT INTO user(user_id,user_name,contact_no,email_id,password) values ('"+str(details[0])+"','"+str(details[1])+"','"+str(details[2])+"','"+str(details[3])+"','"+str(details[4])+"');"
    conn.execute(command)
    conn.commit()






if __name__ == '__main__':
    app.run(debug=True)
