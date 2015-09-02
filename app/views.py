from app import app
from flask import render_template, redirect, url_for, request, session, send_file
from app.controllers.candidate_match import CandidateMatcher
from app.controllers.log_to_s3 import CSVRecorder, S3Connector
import os, datetime

@app.route("/")
def front():
    return render_template("splash.html", first="", fp=0, second="", sp=0, third="", tp=0)

@app.route("/<first>/<fp>/<second>/<sp>/<third>/<tp>", methods=["GET"])
def splash(first, fp, second, sp, third, tp):
    return render_template("splash.html", first=first, fp=float(fp), second=second, sp=float(sp), third=third, tp=float(tp))

@app.route("/survey", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        num_questions = 15
        matcher = CandidateMatcher(num_questions)
        deviation_rankings = matcher.get_match(request.form)

        answers = []
        percentages = []
        for party in deviation_rankings:
            percentages.append((party["short"], party["deviation"]))
        for i in range(1, num_questions + 1):
            result = request.form.getlist(str(i))
            answers.append(result)
        now = "-".join(datetime.datetime.strftime(datetime.datetime.now(), "%Y, %m, %d, %H, %M, %S").split(", "))
        pckg = [now] + answers + percentages

        print pckg

        print "Recording answer"
        recorder = CSVRecorder()
        recorder.record_answer(pckg)
        print "Recording done"

        print "=============================="

        print "Uploading"
        connector = S3Connector()
        connector.upload()
        print "Upload done"

        return render_template("answer.html", deviation_rankings=deviation_rankings)
    else:
        questions = [str(i) for i in range(1, 16)]
        return render_template("index.html", questions=questions, work="works?")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/image")
def image():
    return send_file("static\\img\\logo.png")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
