# https://pythonspot.com/flask-web-app-with-python/
# https://blog.hyperiondev.com/index.php/2018/02/01/deploy-machine-learning-model-flask-api/


from sys import argv
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

import pickle
from sklearn import linear_model
from sklearn.externals import joblib

import numpy as np
import imageio


app = Flask(__name__)
scriptName = argv[0]

@app.route("/")
def hello():
    retString = 'now running ... '+scriptName
    return retString

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method=='POST':
        file = request.files['image']
        if not file: 
            return render_template('index.html', label="No file")
        #f = 'datafiles/'+str(file.filename)
        #file.save(f)
        
        img = imageio.imread(file)
        img = img[:,:,:3]
        img = img.reshape(1, -1)
        prediction = model.predict(img)
        label = str(np.squeeze(prediction))
        if label=='10': 
            label='0'
        return render_template('index.html', label=label, file=file)

if __name__ == "__main__":
    model = joblib.load('datafiles/ic-model.pkl')
    app.run(host="0.0.0.0")
