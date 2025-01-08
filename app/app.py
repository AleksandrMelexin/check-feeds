from flask import Flask, request, render_template
import classes.processing as processing
import json
import os

# isDebug = os.environ.get("CHECK_FEEDS_IS_DEBUG", "True") == "False"
isDebug = os.getenv("CHECK_FEEDS_IS_DEBUG") or "True"
app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    json_data = {}
    return render_template('index.html', json_data=json_data)

@app.route("/check", methods=["POST"])
def check():
    postData = request.get_json()
    process = processing.FeedProcessing(postData["url"])
    return process.process()

if __name__ == '__main__':
    app.run(debug=isDebug) 