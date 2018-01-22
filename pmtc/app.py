from flask import Flask, render_template, request
import sys
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/lol")
def lol():
    return render_template("lol.html")

@app.route("/lol", methods=["POST"])
def lol_pmt(result=None):
    if request.method == "POST":
        url = request.form["match-history"]
        result = subprocess.check_output([sys.executable, "pmtc_lol.py",
            url]).decode("ascii")
    return render_template("lol.html", result=result)

@app.route("/csgo")
def csgo():
    return render_template("csgo.html")

if __name__ == '__main__':
    app.run(debug=True)