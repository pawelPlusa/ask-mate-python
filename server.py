from flask import Flask, render_template, request, redirect
import connection
from data_manager import QUESTIONS

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/list")
def show_questions_list():
    sorted_questions = sorted(QUESTIONS, key= lambda i: i['submission_time'], reverse=1)
    return render_template("list.html", sorted_questions = sorted_questions )

@app.route("/list/<sorted_by>/<int:direction>")
def show_questions(sorted_by,direction):
    sorted_questions = sorted(QUESTIONS, key= lambda i: i[sorted_by], reverse= direction)
    return render_template("list.html", sorted_questions=sorted_questions)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )