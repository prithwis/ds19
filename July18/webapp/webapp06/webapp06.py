#usage
#browser http://127.0.0.1/predict?m1=2&m2=3
#
from sys import argv
# load Flask 
import flask
app = flask.Flask(__name__)

scriptName = argv[0]



@app.route("/")
def hello():
    retString = 'now running ... '+scriptName
    return retString

# define a predict function as an endpoint
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}
    # get the request parameters
    params = flask.request.json
    if (params == None):
        params = flask.request.args
    # if parameters are found, echo the msg parameter 
    if (params != None):
        data["m1"] = params.get("m1")
        data["m2"] = params.get("m2")
        data["success"] = True
    # return a response in json format 
    return flask.jsonify(data)
# start the flask app, allow remote connections
app.run(host='0.0.0.0')
