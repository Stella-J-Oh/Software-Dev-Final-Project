'''
Team xoxo :: Stella Oh, Constance Chen, Winnie Huang, Helena Williams
SoftDev
P3: ArRESTed Development, JuSt in Time
2021-04-21
'''

from flask import Flask, render_template, request, session
import os
import sqlite3
import urllib.request
import json

#Create db for user information
db = sqlite3.connect("p0database.db")
c = db.cursor()
#c.execute("DROP TABLE IF EXISTS stories") #for changing columns
#c.execute("DROP TABLE IF EXISTS users") #for changing columns
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)""")
c.execute("""CREATE TABLE IF NOT EXISTS activities (activity text, type text, participants text)""")
c.execute("""CREATE TABLE IF NOT EXISTS cats (cat text)""")
c.execute("""CREATE TABLE IF NOT EXISTS dogs  (dog text)""")
c.execute("""CREATE TABLE IF NOT EXISTS advices (advice text)""")
c.execute("""CREATE TABLE IF NOT EXISTS bmActivities (user_id text, activity text, type text, participants text)""")
c.execute("""CREATE TABLE IF NOT EXISTS bmCats (user_id text, cat text)""")
c.execute("""CREATE TABLE IF NOT EXISTS bmDogs (user_id text, dog text)""")
db.commit()
db.close()