from app import app
from flask import render_template, redirect, url_for, request, session, send_file
from app.controllers.candidate_match import CandidateMatcher
from app.controllers.log_to_s3 import CSVRecorder, S3Connector
import os, datetime

@app.route("/")
def front():
    return render_template("splash.html", first="", fp=0, second="", sp=0, third="", tp=0)

@app.route("/ma")
def splash_ma():
    return render_template("splash_ma.html", first="", fp=0, second="", sp=0, third="", tp=0)

@app.route("/tm")
def splash_tm():
    return render_template("splash_tm.html", first="", fp=0, second="", sp=0, third="", tp=0)

@app.route("/ch")
def splash_ch():
    return render_template("splash_ch.html", first="", fp=0, second="", sp=0, third="", tp=0)

@app.route("/<first>/<fp>/<second>/<sp>/<third>/<tp>", methods=["GET"])
def splash(first, fp, second, sp, third, tp):
    return render_template("splash.html", first=first, fp=float(fp), second=second, sp=float(sp), third=third, tp=float(tp))

def process_answers(request, language):
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
    pckg = [now] + answers + percentages + [language]

    try:
        print "Recording answer"
        recorder = CSVRecorder()
        recorder.record_answer(pckg)
        print "Recording done"
    except:
        print "Failed to record"

    print "=============================="

    try:
        print "Uploading"
        connector = S3Connector()
        connector.upload()
        print "Upload done"
    except:
        print "Failed to upload"
    return deviation_rankings

@app.route("/survey", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        deviation_rankings = process_answers(request, "en")
        return render_template("answer.html", deviation_rankings=deviation_rankings)
    else:
        questions = [str(i) for i in range(1, 16)]
        return render_template("index.html", questions=questions)

@app.route("/survey/ma", methods=["GET", "POST"])
def survey_ma():
    if request.method == "POST":
        deviation_rankings = process_answers(request, "ma")
        return render_template("answer_malay.html", deviation_rankings=deviation_rankings)
    else:
        questions = [str(i) for i in range(1, 16)]
        return render_template("survey_malay.html", questions=questions)

@app.route("/survey/ch", methods=["GET", "POST"])
def survey_ch():
    if request.method == "POST":
        deviation_rankings = process_answers(request, "ch")
        return render_template("answer_chinese.html", deviation_rankings=deviation_rankings)
    else:
        questions = [str(i) for i in range(1, 16)]
        return render_template("survey_chinese.html", questions=questions)

@app.route("/survey/tm", methods=["GET", "POST"])
def survey_tm():
    if request.method == "POST":
        deviation_rankings = process_answers(request, "ta")
        return render_template("answer_tamil.html", deviation_rankings=deviation_rankings)
    else:
        questions = [str(i) for i in range(1, 16)]
        return render_template("survey_tamil.html", questions=questions)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/about/ma")
def about_ma():
    return render_template("about_malay.html")

@app.route("/about/ch")
def about_ch():
    return render_template("about_chinese.html")

@app.route("/about/tm")
def about_tm():
    return render_template("about_tamil.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
