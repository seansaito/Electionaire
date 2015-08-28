from app import app
from flask import render_template, redirect, url_for, request, session
from app.controllers.candidate_match import CandidateMatcher
from app.controllers.log_to_s3 import CSVRecorder, S3Connector
import datetime

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        num_questions = 3
        matcher = CandidateMatcher(num_questions)
        thing = matcher.get_match(request.form)
        now = "-".join(datetime.datetime.strftime(datetime.datetime.now(), "%Y, %m, %d, %H, %M, %S").split(", "))

        answers = []
        for i in range(1, num_questions + 1):
            result = request.form.getlist(str(i))
            answers.append(result)
        pckg = [now] + answers + [thing]

        print "Recording answer"
        recorder = CSVRecorder()
        recorder.record_answer(pckg)
        print "Recording done"

        print "=============================="

        print "Uploading"
        connector = S3Connector()
        connector.upload()
        print "Upload done"

        return render_template("answer.html", thing=thing)
    else:
        return render_template("index.html")
