from flask import Flask, request
import classes.processing as processing
import json
import os

# isDebug = os.environ.get("CHECK_FEEDS_IS_DEBUG", "True") == "False"
isDebug = os.getenv("CHECK_FEEDS_IS_DEBUG") or "True"
app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/check", methods=["POST"])
def check():
    postData = request.get_json()
    process = processing.FeedProcessing(postData["url"])
    return process.process()

if __name__ == '__main__':
    app.run(debug=isDebug) 