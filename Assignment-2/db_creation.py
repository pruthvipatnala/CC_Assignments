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
             PRIMARY KEY(actID),\
             FOREIGN KEY(category_name) REFERENCES category(category_name) ON DELETE CASCADE,\
             FOREIGN KEY(user_name) REFERENCES user(user_name) ON DELETE CASCADE);")

conn.commit()


#category table insertions
commands = ["INSERT INTO category values('abc','6');","INSERT INTO category values('xyz','1');"]
for i in commands:
	conn.execute(i)
	conn.commit()



#act table insertions
commands = ["INSERT INTO act values ('abc','1','abc','xyz','bla','2','gsgwt43523f');","INSERT INTO act values ('abc','2','ab','sdfa','bla','3','wt43523f');","INSERT INTO act values ('xyz','3','abc','mlp','bla','10','fasdfa');",\
			"INSERT INTO act values ('abc','4','hi','my','name','2','g23f');","INSERT INTO act values ('abc','5','sup','my','name','100','blabla');",\
			"INSERT INTO act values ('abc','6','no','my','name','19','g2afaa3f');","INSERT INTO act values ('abc','7','SDJ','mklpo','nae','54','g2asd3f');"]
for i in commands:
	conn.execute(i)
	conn.commit()



