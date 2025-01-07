from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/check", methods=["POST"])
def check():
    return "<p>Hello from POST</p>"