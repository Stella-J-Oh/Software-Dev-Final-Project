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

app = Flask(__name__)
app.secret_key = os.urandom(32) #need this, if we didn't include this it would produce a runtime error

#Checks if user is in session
@app.route("/", methods = ['GET', 'POST']) #methods=['GET', 'POST']
def disp_loginpage():

    if "user" in session:
        return render_template('homepage.html', user = session["user"])
    else:
        return render_template('login.html')

#Routes user to registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    return render_template('register.html')

#Registration for new user, stores user info into users db
@app.route("/register_auth", methods = ['GET', 'POST'])
def registerConfirming():
    db = sqlite3.connect("p0database.db")
    c1 = db.cursor()

    #gets all the data from the register.html form to check if they exist/match
    u = request.form['new_username']
    p = request.form['new_password_1']
    p1 = request.form['new_password_2']
    c = ''

    #Gets a list of all the registered usernames to check later on
    usernames_list = []
    for x in c1.execute("SELECT username FROM users;"):
        usernames_list.append(x[0])

    if len(u.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid username, try again")
    elif len(p.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid password, try again")
    #Checks if the username exists
    elif u in usernames_list:
        return render_template('register.html', error_type = "Username already exists, try again")
    #Checks if the passwords match
    elif p != p1:
        return render_template('register.html', error_type = "Passwords do not match, try again")
    #If both pass, it adds the newly registered user and directs the user to the login page
    else:
        c1.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        db.commit()
        return render_template("login.html", error_type = "Please login with your new account")


#Checks credentials of login attempt
@app.route("/auth", methods = ['GET', 'POST']) # methods=['GET', 'POST']
def welcome():
    db = sqlite3.connect("p0database.db")
    c2 = db.cursor()
    username = request.form['username']
    password = request.form['password']

    u_list = []
    for x in c2.execute("SELECT username FROM users"):
        for y in x:
            u_list.append(y)
    p_list = []
    for a in c2.execute("SELECT password FROM users"):
        for b in a:
            p_list.append(b)

    if username in u_list and password in p_list:
        session["user"] = username
        return render_template('homepage.html', user = username, message = "Your Login Has Been Successful! \(^-^)/")
    else:
        return render_template('login.html', error_type = "Invalid login attempt, please try again.")

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

@app.route("/saveAct", methods = ['GET', 'POST'])
def saveActivity():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    user_id = session.get("user")
    actList = c.execute('SELECT * FROM activities ORDER BY activity DESC LIMIT 1;')
    actList = c.fetchone()
    actAct = actList[0]
    actType = actList[1]
    actPart = actList[2]

    ##add to db
    command = 'INSERT INTO bmActivities VALUES ("{}","{}", "{}", "{}");'.format(user_id, actAct, actType, actPart)
    c.execute(command)
    ##commit to db
    db.commit()

    return gotoExplore() 

@app.route("/saveDog", methods = ['GET', 'POST'])
def saveDogImg():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    user_id = session.get("user")
    dogList = c.execute('SELECT * FROM dogs ORDER BY dog DESC LIMIT 1;')
    dogList = c.fetchone()
    url = dogList[0]

    ##add to db
    command = 'INSERT INTO bmDogs VALUES ("{}","{}");'.format(user_id, url)
    c.execute(command)
    ##commit to db
    db.commit()

    return Dogs() 

@app.route("/saveCat", methods = ['GET', 'POST'])
def saveCatImg():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()

    user_id = session.get("user")
    catList = c.execute('SELECT * FROM cats ORDER BY cat DESC LIMIT 1;')
    catList = c.fetchone()
    url = catList[0]

    ##add to db
    command = 'INSERT INTO bmCats VALUES ("{}","{}");'.format(user_id, url)
    c.execute(command)
    ##commit to db
    db.commit()

    return Cats() 

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
    command = 'INSERT INTO advices VALUES ("{}");'.format(adviceQ)
    c.execute(command)

    ##activity
    act = urllib.request.urlopen("http://www.boredapi.com/api/activity/")
    actresponse = act.read() #read the api
    actdata = json.loads(actresponse)
    ##variables
    activity = actdata['activity']
    actType = actdata['type']
    participants = actdata['participants']
    ##add to db
    command = 'INSERT INTO activities VALUES ("{}", "{}", "{}" );'.format(activity, actType, participants)
    c.execute(command)

    db.commit()

    return render_template('explore.html', advice = adviceQ, activity = activity, type = actType, participants = participants)    

@app.route("/dogs", methods = ['GET', 'POST'])
def Dogs():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()
    
    u = urllib.request.urlopen("https://dog.ceo/api/breeds/image/random")
    response = u.read() #read the api
    data = json.loads(response)    
    pic = data['message']
    ##add to db
    command = 'INSERT INTO dogs VALUES ("{}");'.format(pic)
    c.execute(command)
    ##commit to db
    db.commit()
    
    return render_template('dogs.html', pic = pic)

# read key_api0.txt file 
file = open("keys/key_api0.txt", "r")
api_key = file.read()
file.close()

@app.route("/cats", methods = ['GET', 'POST'])
def Cats():
    db = sqlite3.connect("p0database.db")
    c = db.cursor()
    
    u = urllib.request.urlopen("https://api.thecatapi.com/v1/images/search?api_key=" + api_key) #open the api URL added with the key
    response = u.read() #read the api
    data = json.loads(response)
    pic = data[0]['url']
    ##add to db
    command = 'INSERT INTO cats VALUES ("{}");'.format(pic)
    c.execute(command)
    ##commit to db
    db.commit()
    return render_template("cats.html", pic = pic) #load the html on the website

#Displays login page and removes user from session
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop("user", None) #removes the session
    return render_template('login.html')

if __name__ == "__main__": # true is this file is NOT imported
    app.debug = True #enable auto-reload upon code change
    app.run()