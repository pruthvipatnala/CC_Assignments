import sqlite3 as sql

conn=sql.connect("assign.db")

conn.execute("CREATE TABLE user (\
             user_name TEXT NOT NULL,\
             password TEXT NOT NULL,\
             PRIMARY KEY(user_name));")

conn.commit()
conn.execute("CREATE TABLE category (\
             category_name TEXT NOT NULL,\
             act_count TEXT NOT NULL,\
             PRIMARY KEY(category_name));")

conn.commit()


conn.execute("CREATE TABLE act (\
             category_name TEXT NOT NULL,\
             actID TEXT NOT NULL,\
             user_name TEXT NOT NULL,\
             time_stamp TEXT NOT NULL,\
             caption TEXT NOT NULL,\
             upvotes TEXT NOT NULL,\
             imgB64 TEXT NOT NULL,\
             PRIMARY KEY(actID));")

conn.commit()


commands = ["INSERT INTO act values ('abc','1','abc','xyz','bla','2','gsgwt43523f');","INSERT INTO act values ('abc','2','ab','sdfa','bla','3','wt43523f');","INSERT INTO act values ('xyz','3','abc','mlp','bla','10','fasdfa');"]
for i in commands:
	conn.execute(i)
	conn.commit()



