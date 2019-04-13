import sqlite3 as sql

conn=sql.connect("assign.db")
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
             FOREIGN KEY(category_name) REFERENCES category(category_name) ON DELETE CASCADE);")

conn.commit()

conn.execute("CREATE TABLE count (\
			count TEXT NOT NULL);")

conn.commit()

conn.execute("INSERT INTO count VALUES('0');")

conn.commit()
