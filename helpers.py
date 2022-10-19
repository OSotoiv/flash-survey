from flask import session
from surveys import surveys


def valid_answer(survey, answer, id):
    """validates if submitted answer is in the questions choices
    also checks if responses is still excepting answers"""
    # make sure cookie have not been cleared mid survey
    if session[survey].get('responses') or session[survey].get('responses') == []:
        # make sure user is submitting the
        if id == len(session[survey]["responses"]):
            # check if session responses does not exceed amount of questions
            if len(session[survey]["responses"]) < len(surveys[survey].questions):
                # check returned answer is valid
                if answer in surveys[survey].questions[id].choices:
                    return True
    return False


def set_session(survey_title):
    """set session for user selected survey"""
    session[survey_title] = {'responses': [], 'completed': False}


def set_session_res(survey, answer):
    """update response for user selected survey"""
    res = session[survey]['responses']
    res.append(answer)
    session[survey]['responses'] = res
    return True
