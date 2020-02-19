"""
Questions format:
[{id: str, submission_time: time_stamp (int), view_number: int, vote_number: int, title: str, message: str, image: url(str)},
...
]

Answers format:
[{id: str,submission_time: time_stamp (int), vote_number: int, question_id: int, message: str, image: url(str)},
...
]
"""

from flask import Flask, render_template, request, redirect
import data_manager
import util

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/list")
def show_questions_list():
    sorted_questions = sorted(data_manager.QUESTIONS, key= lambda i: i['submission_time'], reverse=1)
    return render_template("list.html", sorted_questions = sorted_questions )

@app.route("/list/<sorted_by>/<int:direction>")
def show_questions(sorted_by,direction):
    sorted_questions = sorted(data_manager.QUESTIONS, key= lambda i: i[sorted_by], reverse= direction)
    return render_template("list.html", sorted_questions=sorted_questions)



@app.route("/question/<question_id>")
def show_answers(question_id):
    question = str(data_manager.QUESTIONS[int(question_id)]['title'])
    answers = util.find_answers_by_question(question_id, data_manager.ANSWERS)

    return render_template('questions.html', question=question, answers=answers)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )
