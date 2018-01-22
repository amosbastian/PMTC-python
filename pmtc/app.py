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

@app.route("/lol/pmt", methods=["GET"])
def lol_pmt(result=None):
    url = request.args.get("match-history", None)
    if url:
        result = subprocess.check_output([sys.executable, "pmtc_lol.py", url])
    return render_template("lol.html", result=result)

@app.route("/csgo")
def csgo():
    return render_template("csgo.html")

if __name__ == '__main__':
    app.run(debug=True)