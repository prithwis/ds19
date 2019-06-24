# tutorial from https://www.houseofbots.com/news-detail/4528-1-how-to-deploy-keras-deep-learning-models-with-flask
# docker build -t calcutta/de-apptfk00 .
# docker run --rm --name praxis007 -p 8888:5000 calcutta/de-apptfk00
#

from sys import argv

# Load libraries

import flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

# instantiate flask 
app = flask.Flask(__name__)
#app = Flask(__name__)
scriptName = argv[0]

# we need to redefine our metric function in order 
# to use it when loading the model 
def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc
# load the model, and pass in the custom metric function
global graph
graph = tf.get_default_graph()
model = load_model('./games.h5', custom_objects={'auc': auc})


@app.route("/")
def hello():
    retString = 'running '+scriptName+' go to http://192.168.99.100:8888/home for more information'
    return retString

@app.route('/home')
def home():
    return render_template('home.html')

# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}
    params = flask.request.json
    
    if (params == None):
       params = flask.request.args
       
    #params = {'g1':1,'g2':0,'g3':0,'g4':0,'g5':0,'g6':0,'g7':0,'g8':0,'g9':0,'g10':0}
    # if parameters are found, return a prediction
    if (params != None):
        x=pd.DataFrame.from_dict(params, orient='index').transpose()
        with graph.as_default():
            data["prediction"] = str(model.predict(x)[0][0])
            data["success"] = True
    # return a response in json format 
    return flask.jsonify(data)  

# define a predict function as an endpoint 
@app.route("/predict2", methods=["GET","POST"])
def predict2():
    data = {"success": False}
    params = flask.request.json
    
    if (params == None):
       params = flask.request.args
       
    #params = {'g1':1,'g2':0,'g3':0,'g4':0,'g5':0,'g6':0,'g7':0,'g8':0,'g9':0,'g10':0}
    # if parameters are found, return a prediction
    if (params != None):
        x=pd.DataFrame.from_dict(params, orient='index').transpose()
        with graph.as_default():
            prediction = str(model.predict(x)[0][0])
            status = True
    return render_template('predict2.html',**locals())
      
# start the flask app, allow remote connections 
app.run(host='0.0.0.0')