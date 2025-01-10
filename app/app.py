from flask import Flask, request, render_template
import classes.processing as processing
import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Feeds(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=False)

isDebug = os.getenv("CHECK_FEEDS_IS_DEBUG") or True
if isDebug == "0":
    isDebug = False
else:
    isDebug = True
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "db",'db.sqlite')
db.init_app(app)
     
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