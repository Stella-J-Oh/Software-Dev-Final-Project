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
import dbsetup
from app import app

#Displays homepage when successful login
@app.route("/homepage", methods = ['GET', 'POST'])
def returnHome():
    db = sqlite3.connect("p0database.db")
    c4 = db.cursor()

    userList = []
    for x in c4.execute("SELECT username FROM users"):
        userList.append(x[0])
    user_index = userList.index(session["user"])

    return render_template('homepage.html', user = session["user"])

#explore page
@app.route("/explore", methods = ['GET', 'POST'])
def gotoExplore():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()
    
    ##advice slips
    u = urllib.request.urlopen("https://api.adviceslip.com/advice")
    response = u.read() #read the api
    data = json.loads(response)
    #variable
    adviceQ = data['slip']['advice']
    ##add to db
    c.execute('INSERT INTO advices (advice) VALUES (?)',(adviceQ,))
    
    ##activity
    act = urllib.request.urlopen("http://www.boredapi.com/api/activity/")
    actresponse = act.read() #read the api
    actdata = json.loads(actresponse)
    ##variables
    activity = actdata['activity']
    actType = actdata['type']
    participants = actdata['participants']
    ##add to db
    c.execute('INSERT INTO activities (activity, type, participants) VALUES (?, ?, ?)', (activity, actType, participants))

    db.commit()
    db.close()

    return render_template('explore.html', advice = adviceQ, activity = activity, type = actType, participants = participants)

#bookmarking activity
@app.route("/saveAct", methods = ['GET', 'POST'])
def saveActivity():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    username = session.get("user")
    actList = c.execute('SELECT * FROM activities ORDER BY activity DESC LIMIT 1;')
    actList = c.fetchone()
    actAct = actList[0]
    actType = actList[1]
    actPart = actList[2]

    ##add to db
    c.execute('INSERT INTO bmActivities (user_id, activity, type, participants) VALUES (?,?,?,?)',(username, actAct, actType, actPart))
    ##commit to db
    db.commit()
    db.close()

    return gotoExplore() 

#displays bookmarked activities
@app.route("/bookmarked-activities", methods = ['GET', 'POST'])
def bookmarkedActivities():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    user_id = session.get("user")
    c.execute('SELECT * FROM bmActivities')
    actArr = []
    for row in c:
        if (row[0] == user_id):
            actRow = []
            actRow.append(row[1])
            actRow.append(row[2])
            actRow.append(row[3])
            actArr.append(actRow) 
    return render_template('bmactivities.html', actArr = actArr)

#bookmarks cat image
@app.route("/saveCat", methods = ['GET', 'POST'])
def saveCatImg():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    username = session.get("user")
    catList = c.execute('SELECT * FROM cats ORDER BY cat DESC LIMIT 1;')
    catList = c.fetchone()
    url = catList[0]

    ##add to db
    c.execute('INSERT INTO bmCats (user_id, cat) VALUES (?,?)',(username, url))
    ##commit to db
    db.commit()
    db.close()

    return Cats() 

#displays bookmarked cats
@app.route("/bookmarked-cats", methods = ['GET', 'POST'])
def bookmarkedCats():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    user_id = session.get("user")
    c.execute('SELECT * FROM bmCats')
    catArr = []
    for row in c:
        if (row[0] == user_id):
            catArr.append(row[1]) 
    return render_template('bmcats.html', catArr = catArr)

#bookmarks dogs
@app.route("/saveDog", methods = ['GET', 'POST'])
def saveDogImg():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    username = session.get("user")
    dogList = c.execute('SELECT * FROM dogs ORDER BY dog DESC LIMIT 1;')
    dogList = c.fetchone()
    url = dogList[0]

    ##add to db
    c.execute('INSERT INTO bmDogs (user_id, dog) VALUES (?,?)',(username, url))
    ##commit to db
    db.commit()
    db.close()

    return Dogs() 

#displays bookmarked dogs
@app.route("/bookmarked-dogs", methods = ['GET', 'POST'])
def bookmarkedDogs():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    user_id = session.get("user")
    c.execute('SELECT * FROM bmDogs')
    dogArr = []
    for row in c:
        if (row[0] == user_id):
            dogArr.append(row[1]) 
    return render_template('bmdogs.html', dogArr = dogArr)    

#displays dog images
@app.route("/dogs", methods = ['GET', 'POST'])
def Dogs():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()
    
    u = urllib.request.urlopen("https://dog.ceo/api/breeds/image/random")
    response = u.read() #read the api
    data = json.loads(response)    
    pic = data['message']
    ##add to db
    c.execute('INSERT INTO dogs (dog) VALUES (?);',(pic,))
    ##commit to db
    db.commit()
    db.close()
    
    return render_template('dogs.html', pic = pic)

# read key_api0.txt file 
file = open("keys/key_api0.txt", "r")
api_key = file.read()
file.close()

#displays cat image
@app.route("/cats", methods = ['GET', 'POST'])
def Cats():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()
    
    u = urllib.request.urlopen("https://api.thecatapi.com/v1/images/search?api_key=" + api_key) #open the api URL added with the key
    response = u.read() #read the api
    data = json.loads(response)
    pic = data[0]['url']
    ##add to db
    c.execute('INSERT INTO cats (cat) VALUES (?);',(pic,))
    ##commit to db
    db.commit()
    db.close()
    return render_template("cats.html", pic = pic) #load the html on the website

#Displays login page and removes user from session
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop("user", None) #removes the session
    return render_template('login.html')

if __name__ == "__main__": # true is this file is NOT imported
    app.debug = True #enable auto-reload upon code change
    app.run()