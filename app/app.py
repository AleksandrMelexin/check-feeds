import os
import time

import redis
from flask import Flask, request, render_template, session, send_from_directory
from flask_apscheduler import APScheduler
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

import classes.processing as processing
import classes.reporting as reporting

isDebug = os.getenv("CHECK_FEEDS_IS_DEBUG") or True
if isDebug == "0":
    isDebug = False
else:
    isDebug = True

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
Session(app)
db = SQLAlchemy()

if os.getenv("DB_TYPE") == "postgres":
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}"
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'db.sqlite')
db.init_app(app)

baseDir = os.path.dirname(os.path.abspath(__file__))
tempDir = os.path.join(baseDir, "temp")
FILE_TIME_LIMIT = 3600


def deleteOldFiles():
    now = time.time()
    for filename in os.listdir(tempDir):
        filePath = os.path.join(tempDir, filename)
        if os.path.isfile(filePath):
            fileTime = os.path.getctime(filePath)
            if now - fileTime > FILE_TIME_LIMIT:
                try:
                    os.remove(filePath)
                    print(f"Удален файл: {filePath}")
                except Exception as e:
                    print(f"Ошибка при удалении {filePath}: {e}")


scheduler.add_job(id="deleteOldFiles", func=deleteOldFiles, trigger="interval", minutes=5)


@app.route("/", methods=["GET", "POST"])
def check_feeds():
    json_data = {}
    if request.method == "POST":
        formData = request.form.to_dict()
        process = processing.FeedProcessing(formData["inputUrl"])
        json_data = process.process
    return render_template("index.html", json_data=json_data)


@app.route("/check", methods=["POST"])
def check():
    formData = request.form.to_dict()
    process = processing.FeedProcessing(formData["inputUrl"])
    return process.process


@app.route("/report", methods=["GET"])
def get_report():
    report = reporting.FeedReporting()
    report.createReport()
    fileName = session.get("fileName")
    return send_from_directory(tempDir, fileName, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    scheduler.start()
    app.run(debug=isDebug, host="0.0.0.0", port=int(os.getenv("FLASK_PORT")))
