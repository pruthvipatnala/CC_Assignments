import sqlite3 as sql

conn=sql.connect("assign.db")

conn.execute("CREATE TABLE user (\
             user_name TEXT NOT NULL,\
             password TEXT NOT NULL,\
             PRIMARY KEY(user_name));")

conn.commit()
