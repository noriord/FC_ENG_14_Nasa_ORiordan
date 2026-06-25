from flask import Flask, render_template

app = Flask(__name__, template_folder="homework")

@app.route("/")
def index_view():
    return render_template("index.html")


@app.route("/history")
def history_view():
    return render_template("history.html")