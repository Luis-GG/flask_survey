from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)





@app.route("/")
def home_page():
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions
    

    return render_template("home_page.html", title=title, instructions=instructions)


@app.route("/start", methods=["POST"])
def start_survey():
    session["responses"] = []

    return redirect("/questions/0")


@app.route("/questions/<int:quest_num>")
def questions(quest_num):

    ##
    if request.path != f"/questions/{len(session['responses'])}" or quest_num > len(surveys.satisfaction_survey.questions):
        flash("INVALID URL")
        return redirect(f"/questions/{len(session['responses'])}")
        
    ##
    question = surveys.satisfaction_survey.questions[quest_num]
    choices = question.choices


    return render_template("questions.html", question=question, quest_num=quest_num, choices=choices)


@app.route("/answer", methods=["POST","GET"])
def answer():
    response_session_list = session['responses']
    response_session_list.append(request.form["answer"])
    session['responses'] = response_session_list

    if(len(session['responses']) == len(surveys.satisfaction_survey.questions)):
        return redirect("/completed")

    return redirect(f"/questions/{len(session['responses'])}")


@app.route("/completed")
def thank_you():

    return render_template("thanks.html")
