"""
Questions format:
[{id: int, submission_time: time_stamp (int), view_number: int, vote_number: int, title: str, message: str, image: url(str)},
...
]

Answers format:
[{id: int,submission_time: time_stamp (int), vote_number: int, question_id: int, message: str, image: url(str)},
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


@app.route("/question/<question>?<sorted=date>")
def show_answers(question_id, sort='date', reverse=True):

    return render_template('list_comments.html', question)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )
