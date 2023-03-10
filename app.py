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
    global responses
    responses = []
    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def redirect_to_first_question():
    """When a survey is started, redirect the user to the first question"""

    question_number = len(responses)
    return redirect(f"/questions/{question_number}")


@app.get("/questions/<int:question_number>")
def show_question(question_number):
    """Shows the current question for the survey."""

    question = survey.questions[question_number]
    return render_template("question.html", question=question)


@app.post("/answer")
def get_answer_and_redirect():
    """"Stores user answer in responses list, then redirects appropriately:
    to next question if there is one, otherwise to thankyou page
     """

    answer = request.form["answer"]

    responses.append(answer)

    question_number = len(responses)

    if len(responses) == len(survey.questions):
        return redirect("/thankyou")

    return redirect(f"/questions/{question_number}")


@app.get("/thankyou")
def show_thankyou_page():
    """Thanks user and displays all questions and answers"""

    questions = survey.questions

    prompts = [question.prompt for question in questions]

    completed_survey = [item for item in zip(prompts, responses)]

    return render_template("completion.html",
                           completed_survey=completed_survey)
