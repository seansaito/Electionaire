from app import app
from flask import render_template, redirect, url_for, request, session
from app.controllers.candidate_match import CandidateMatcher

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        """
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
        """
        matcher = CandidateMatcher(1)
        thing = matcher.get_match(request.form)

        return render_template("answer.html", thing=thing)
    else:
        return render_template("index.html")
