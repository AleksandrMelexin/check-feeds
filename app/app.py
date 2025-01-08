from flask import Flask, request, render_template
import classes.processing as processing
import json
import os

# isDebug = os.environ.get("CHECK_FEEDS_IS_DEBUG", "True") == "False"
isDebug = os.getenv("CHECK_FEEDS_IS_DEBUG") or True
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    json_data = {}
    if request.method == "POST":
        formData = request.form.to_dict()
        process = processing.FeedProcessing(formData["inputUrl"])
        json_data = process.process()
    return render_template("index.html", json_data=json_data)

@app.route("/check", methods=["POST"])
def check():
    formData = request.form.to_dict()
    process = processing.FeedProcessing(formData["inputUrl"])
    return process.process()

if __name__ == "__main__":
    app.run(debug=isDebug) 