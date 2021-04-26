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
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, contributions text)""")
c.execute("""CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title text, entire text, recent text, contributors text)""")
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
        c1.execute("INSERT INTO users (username, password, contributions) VALUES (?, ?, ?)", (u, p, c))
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

    usersContributions = []
    if username in u_list:
        user_index = u_list.index(username)
        for x in c2.execute("SELECT contributions FROM users"):
            usersContributions.append(x[0])
        user_conts = usersContributions[user_index].split("~")

        if (len(user_conts) >= 1):
            user_conts.pop()

    if username in u_list and password in p_list:
        session["user"] = username
        return render_template('homepage.html', user = username, contribution_list = user_conts, message = "Your Login Has Been Successful! \(^-^)/")
    else:
        return render_template('login.html', error_type = "Invalid login attempt, please try again.")


#Displays homepage when successful login
@app.route("/homepage", methods = ['GET', 'POST'])
def returnHome():
    db = sqlite3.connect("p0database.db")
    c4 = db.cursor()

    usersContributions = []
    userList = []
    for x in c4.execute("SELECT username FROM users"):
        userList.append(x[0])
    user_index = userList.index(session["user"])

    for x in c4.execute("SELECT contributions FROM users"):
        usersContributions.append(x[0])

    user_conts = usersContributions[user_index].split("~")
    if (len(user_conts) >= 1):
        user_conts.pop()

    return render_template('homepage.html', user = session["user"], contribution_list = user_conts)

@app.route("/explore", methods = ['GET', 'POST'])
def gotoExplore():
    return render_template('explore.html')

@app.route("/bookmarked-activities", methods = ['GET', 'POST'])
def bookmarkedActivities():
    return render_template('bmactivities.html')

@app.route("/bookmarked-cats", methods = ['GET', 'POST'])
def bookmarkedCats():
    return render_template('bmcats.html')

@app.route("/bookmarked-dogs", methods = ['GET', 'POST'])
def bookmarkedDogs():
    return render_template('bmdogs.html')

@app.route("/dogs", methods = ['GET', 'POST'])
def Dogs():
    return render_template('dogs.html')

# read key_nasa.txt file 
file = open("keys/key_api0.txt", "r")
api_key = file.read()
file.close()

@app.route("/cats", methods = ['GET', 'POST'])
def Cats():
    u = urllib.request.urlopen("https://api.thecatapi.com/v1/images/search?api_key=" + api_key) #open the api URL added with the key
    response = u.read() #read the api
    data = json.loads(response)
    return render_template("cats.html", pic = data[0]['url']) #load the html on the website

#Displays login page and removes user from session
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop("user", None) #removes the session
    return render_template('login.html')

if __name__ == "__main__": # true is this file is NOT imported
    app.debug = True #enable auto-reload upon code change
    app.run()