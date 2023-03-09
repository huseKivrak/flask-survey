from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def show_start_page():
    """Show the begin page for a survey. Redirects to the first question"""

    return render_template("survey_start.html", s=survey)

@app.post("/begin")
def redirect_to_first_question():
    """When a survey is started, redirect the user to the first question"""

    question_number = len(responses)
    return redirect(f"/questions/{question_number}")


@app.get("/questions/<int:question_number>")
def show_question(question_number):
    """Shows the current question for the survey."""

    q = survey.questions[question_number]
    return render_template("question.html", question=q)
