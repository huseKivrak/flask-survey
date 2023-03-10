from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#responses = []


@app.get("/")
def show_start_page():
    """Show the begin page for a survey."""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def redirect_to_first_question():
    """When a survey is started, redirect the user to the first question"""

    # makes sure our responses are empty before we start the survey
    #responses.clear()

    session["responses"] = []
    session["existence"] = True

    return redirect("/questions/0")


@app.get("/questions/<int:question_number>")
def show_question(question_number):
    """Validates we are allowed to be at this question.
    Shows the current question for the survey if we are allowed.
    Otherwise, send us to the right question, or home if there is no session
    """

    if not session.get("existence"):
        return redirect("/")
    
    num_responses = len(session["responses"])
    if num_responses != question_number:
        return redirect(f"/questions/{num_responses}")

    question = survey.questions[question_number]
    return render_template("question.html", question=question)


@app.post("/answer")
def get_answer_and_redirect():
    """"Stores user answer in responses list, then redirects appropriately:
    to next question if there is one, otherwise to thank you page
     """

    answer = request.form["answer"]

    # can't append directly to the session, so we make a temp list to append to
    temp_responses = session["responses"]
    temp_responses.append(answer)
    session["responses"] = temp_responses

    question_number = len(session["responses"])

    if len(session["responses"]) == len(survey.questions):
        return redirect("/thankyou")

    return redirect(f"/questions/{question_number}")


@app.get("/thankyou")
def show_thankyou_page():
    """Thanks user and displays all questions and answers"""

    questions = survey.questions

    prompts = [question.prompt for question in questions]

    completed_survey = [item for item in zip(prompts, session["responses"])]
    return render_template("completion.html",
                           completed_survey=completed_survey)
