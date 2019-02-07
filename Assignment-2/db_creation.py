#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 20:58:15 2019

@author: pruthvi
"""

import sqlite3 as sql

conn=sql.connect("assign.db")

conn.execute("CREATE TABLE user (\
             user_id TEXT NOT NULL,\
             user_name TEXT,\
             contact_no TEXT UNIQUE NOT NULL,\
             email_id TEXT,\
             password TEXT NOT NULL,\
             PRIMARY KEY(user_id));")

