# https://pythonspot.com/flask-web-app-with-python/

from sys import argv
from flask import Flask, flash, redirect, render_template, request, session, abort

import pickle
from sklearn import linear_model

app = Flask(__name__)
scriptName = argv[0]

@app.route("/")
def hello():
    retString = 'now running ... '+scriptName
    return retString

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/predict1/<featureString>')
def multidata(featureString):
    str1 = featureString
    feature_list = featureString.split(",")
    feature_array = list(map(lambda x : float(x), feature_list))

    model = pickle.load(open("datafiles/lrw-model.pkl","rb"))

    #our model rates the wine based on the input array
    prediction = model.predict([feature_array]).tolist()

    return render_template('predict1.html',**locals())


if __name__ == "__main__":
    app.run(host="0.0.0.0")
