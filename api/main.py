from flask import Flask, request
import classes.processing as processing
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/check", methods=["POST"])
def check():
    postData = request.get_json()
    process = processing.FeedProcessing(postData["url"])
    return process.process() 