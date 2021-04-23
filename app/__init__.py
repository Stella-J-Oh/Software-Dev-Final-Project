'''
Team xoxo :: Stella Oh, Constance Chen, Winnie Huang, Helena Williams
SoftDev
P3: ArRESTed Development, JuSt in Time
2021-04-21
'''

from flask import Flask, render_template
import urllib.request
import json

app = Flask(__name__)
# read key_nasa.txt file 
file = open("keys/key_api0.txt", "r")
api_key = file.read()

@app.route("/")
def root():
    u = urllib.request.urlopen("https://dog.ceo/api/breeds/image/random") #open the api URL added with the key
    response = u.read() #read the api
    data = json.loads(response)
    return render_template("home.html", pic = data['message']) #load the html on the website


if __name__ == "__main__": # true is this file is NOT imported
    app.debug = True #enable auto-reload upon code change
    app.run()