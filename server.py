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
import time
import connection

app = Flask(__name__)

# Paweł

@app.route("/")
def start():
    sorted_questions = sorted(data_manager.QUESTIONS, key= lambda i: i['submission_time'], reverse=1)

    return render_template("index.html", sorted_questions=util.change_time_format(sorted_questions),
                           headers=list(sorted_questions[0].keys())[1:])


@app.route("/delete/<question_id>/<int:confirmation>")
@app.route("/delete/<question_id>")
def delete(question_id=None, confirmation=None, status=None):

    if confirmation:
        del data_manager.QUESTIONS[util.find_index_of_dict_by_id(data_manager.QUESTIONS,question_id)]
        connection.save_file(data_manager.QUESTIONS, data_manager.QUESTION_FILE_PATH)

        return render_template("delete.html", status=1)
    else:
        return render_template("delete.html", question_id=question_id)


# Łukasz

@app.route("/list")
def show_questions_list():
    sorted_questions = sorted(data_manager.QUESTIONS, key=lambda i: i['submission_time'], reverse=1)

    return render_template("list.html", sorted_questions=util.change_time_format(sorted_questions))


@app.route("/list/<sorted_by>/<int:direction>")
def show_questions(sorted_by,direction):
    sorted_questions = sorted(data_manager.QUESTIONS, key=lambda i: i[sorted_by], reverse=direction)

    return render_template("list.html", sorted_questions=util.change_time_format(sorted_questions))


# Tomek

@app.route("/questions/<question_id>")
@app.route("/questions/<question_id>/<sorted_by>/<int:direction>")
@app.route("/questions/<question_id>/<vote>")
def show_answers(question_id, sorted_by=None, direction=0, vote=None):

    question_index = util.find_index_of_dict_by_id(data_manager.QUESTIONS, question_id)
    question_title = data_manager.QUESTIONS[int(question_id)]['title']
    question_message = data_manager.QUESTIONS[int(question_id)]['message']
    answers = util.find_answers_by_question(question_id, data_manager.ANSWERS)

    if vote:
        votes_no = int(data_manager.QUESTIONS[question_index]["vote_number"])
        if vote == "vote_down" and votes_no > 0:
            votes_no -= 1
        elif vote == "vote_up":
            votes_no += 1
        data_manager.QUESTIONS[int(question_index)]["vote_number"] = str(votes_no)
        connection.save_file(data_manager.QUESTIONS, data_manager.QUESTION_FILE_PATH)

        return redirect("/list", code=303)

    if sorted_by in ["submission_time", "vote_number"]:
        answers.sort(key=lambda item: int(item[sorted_by]), reverse=direction)
    elif sorted_by:
        answers.sort(key=lambda item: item[sorted_by], reverse=direction)

    return render_template('questions.html',
                           question_id=question_id, question_title=question_title,
                           question_message=question_message, answers=util.change_time_format(answers),
                           direction=direction)


@app.route("/answer/<question_id>", methods=['GET', 'POST'])
@app.route("/answer/<question_id>/<answer_id>", methods=['GET', 'POST'])
def add_answer(question_id, answer_id=None, answer_message=None):
    question_title = data_manager.QUESTIONS[int(question_id)]['title']

    if request.method == 'POST':
        data_to_save = data_manager.ANSWERS

        if answer_id:
            data_to_save[int(answer_id)]['message'] = request.form['answer_m']
            data_to_save[int(answer_id)]['submission_time'] = str(int(time.time()))
        else:
            data_to_save.append({'id': util.find_next_id(data_to_save),
                                 'submission_time': str(int(time.time())),
                                 'vote_number': '0',
                                 'question_id': question_id,
                                 'message': request.form['answer_m']
                                 })

        connection.save_file(data_to_save, data_manager.ANSWERS_FILE_PATH)

        return redirect('/questions/' + question_id)

    if answer_id:
        answer_message = data_manager.ANSWERS[int(answer_id)]['message']

    return render_template('answer.html',
                           answer_id=answer_id, answer_message=answer_message,
                           question_title=question_title)


# Łukasz

@app.route("/note", methods=['GET', 'POST'])
@app.route("/note/<question_id>", methods=['GET', 'POST'])
def add_question(message=None, title=None, question_id=None):

    if request.method == 'GET' and question_id:
        title = data_manager.QUESTIONS[int(question_id)]["title"]
        message = data_manager.QUESTIONS[int(question_id)]["message"]

    elif request.method == 'POST':
        data_to_save = data_manager.QUESTIONS

        if not question_id:
            question_id = (util.find_next_id(data_to_save))
            print(question_id)
            print(data_to_save)
            data_to_save.append({'id': question_id,
                                 'submission_time': str(int(time.time())),
                                 'view_number': '0',
                                 'vote_number': '0',
                                 'message': request.form['question_m'],
                                 'title': request.form['title_m']
                                 })
        else:
            data_to_save[int(question_id)]['message'] = request.form['question_m']
            data_to_save[int(question_id)]['submission_time'] = str(int(time.time()))
            data_to_save[int(question_id)]['title'] = request.form['title_m']

        connection.save_file(data_to_save, data_manager.QUESTION_FILE_PATH)

        return redirect('/list')

    return render_template('note.html', message=message, title=title, question_id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )
