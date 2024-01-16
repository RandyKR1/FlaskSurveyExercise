from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/intro')
def show_start_up():
    return render_template('survey-intro.html', survey=survey)


@app.route('/start', methods=["POST"]) #this redirect clears the survey of all previous responses by setting responses to a blank list then redirecting to the first question.
def start_survey():
    session[RESPONSES_KEY]=[]
    return redirect('/questions/0')


@app.route("/answer", methods=["POST"])
def handle_questions():
    choice = request.form["answer"] # naming the answers from the form "choices"
    session[RESPONSES_KEY].append(choice) #appending these choices
    
    responses = session[RESPONSES_KEY] # re-declaring the updated list to the variable "responses"
    if (len(responses) == len(survey.questions)):
        return redirect("/complete") #if the lengths are the same, show complete route
    else:
        return redirect(f"/questions/{len(responses)}") # having issues here I think, I am stuck on question 1, qid:0. Seems to be an issue with submit button or this code.
    
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}")
        return redirect(f"/questions/{len(responses)}")
        
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)
    
    

@app.route("/complete")
def complete():
    return render_template("completion.html")