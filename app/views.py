from app import app
from flask import render_template, redirect, url_for, request

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/form", methods=["POST"])
def form():
    result = request.form.getlist("1")
    dog=4
    cat=0

    if len(result) != 2:
        return render_template("index.html")
    
    importance, user_choice = result

    dog_diff = int(importance) * abs(dog - int(user_choice))
    cat_diff = int(importance) * abs(cat - int(user_choice))

    thing = ""

    if dog_diff > cat_diff:
        thing = "cat"
    elif cat_diff > dog_diff:
        thing = "dog"
    else:
        thing = "human"

    return render_template("answer.html", thing=thing)
