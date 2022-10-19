from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys
import helpers

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'survey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar_debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    """show all avalible surveys to user"""
    return render_template('home.html', surveys=surveys)


@app.route('/start/<survey>', methods=['POST'])
def start(survey):
    """Still not sure why this needs to be a post request
    handles starting user selected survey if survery is incomplete"""
    # do not allow user to take the test twice
    if session.get(survey) and session.get(survey)['completed']:
        return redirect(f'/alldone/{survey}')
    # this helper creates a cookie but has not sent the cookie
    helpers.set_session(survey)
    return redirect(f"/questions/{survey}/0")


@app.route('/questions/<survey>/<id>')
def questions(survey, id):
    """show user survey questions in order"""
    id = int(id)
    if len(surveys[survey].questions) == len(session[survey]["responses"]):
        # survey is completed
        flash('Thank You!', "success")
        return redirect(f'/alldone/{survey}')
    elif id == len(session[survey]["responses"]):
        # show user next question
        title = surveys[survey].title
        question = surveys[survey].questions[id]
        return render_template('questions.html', survey=survey, question=question, survey_title=title, id=id)
    else:
        # user seeking questions out of order
        flash('First answer this question', 'error')
        return redirect(f'/questions/{survey}/{len(session[survey]["responses"])}')


@app.route('/answer/<survey>/<id>', methods=['POST'])
def answer(survey, id):
    """handle user submiting answer"""
    answer = request.form.get('answer')
    id = int(id)
    if not session.get(survey):
        # user deleted cookies mid survey
        flash('Did you delete your cookies?', 'error')
        return redirect('/')
    elif answer and helpers.valid_answer(survey, answer, id):
        # ****error****
        # the session will not update unless I use a flash befor redirecting
        helpers.set_session_res(survey, answer)
        # Empty flash is to allow the session cookies time to update. Wasnt updating without it
        flash('', '')
        return redirect(f'/questions/{survey}/{len(session[survey]["responses"])}')
    else:
        flash('Something went wrong', 'warning')
        return redirect(f'/questions/{survey}/{len(session[survey]["responses"])}')


@app.route('/alldone/<survey>')
def alldone(survey):
    # make sure user is not going to this route manualy
    if len(surveys[survey].questions) == len(session[survey]["responses"]):
        session[survey]['completed'] = True
        return render_template('alldone.html', survey_title=survey, responses=session[survey]['responses'])
    flash('Your not done!', 'warning')
    return redirect(f'/questions/{survey}/{len(session[survey]["responses"])}')
