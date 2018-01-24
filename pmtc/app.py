from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError

import sys
import subprocess

app = Flask(__name__)
app.config["SECRET_KEY"] = "fuckoff"

test = True

@app.route("/")
def index():
    return render_template("index.html")

def is_matchhistory(form, field):
    if not "https://matchhistory" in field.data and len(field.data) < 90:
        raise ValidationError("Must be a valid match history URL!")

class MatchHistoryForm(FlaskForm):
    matchhistory = StringField("matchhistory", validators=[InputRequired(),
        is_matchhistory], render_kw={"placeholder": "Match history"})

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/lol", methods=["GET", "POST"])
def lol():
    form = MatchHistoryForm()

    if form.validate_on_submit():
        url = form.matchhistory.data
        result = subprocess.check_output([sys.executable, "pmtc_lol.py",
            url]).decode("ascii")
        return render_template("lol.html", form=form, result=result)
    return render_template("lol.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/csgo")
def csgo():
    return render_template("csgo.html")

if __name__ == '__main__':
    app.run(debug=True)