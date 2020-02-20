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
    return render_template("index.html", sorted_questions=sorted_questions)

# Łukasz

@app.route("/list")
def show_questions_list():
    sorted_questions = sorted(data_manager.QUESTIONS, key= lambda i: int(i['submission_time']), reverse=1)
    return render_template("list.html", sorted_questions = sorted_questions )


@app.route("/list/<sorted_by>/<int:direction>")
def show_questions(sorted_by,direction):
    sorted_questions = sorted(data_manager.QUESTIONS, key= lambda i: i[sorted_by], reverse= direction)
    return render_template("list.html", sorted_questions=sorted_questions)


# Tomek

@app.route("/questions/<question_id>")
def show_answers(question_id):
    question_id = data_manager.QUESTIONS[int(question_id)]['id']
    question_title = data_manager.QUESTIONS[int(question_id)]['title']
    question_message = data_manager.QUESTIONS[int(question_id)]['message']
    answers = util.find_answers_by_question(question_id, data_manager.ANSWERS)
    print(answers)

    return render_template('questions.html',
                           question_id=question_id, question_title=question_title,
                           question_message=question_message, answers=answers)


@app.route("/answer/<question_id>", methods=['GET', 'POST'])
@app.route("/answer/<question_id>/<answer_id>", methods=['GET', 'POST'])
def add_answer(question_id, answer_id=None, answer_message=None):

    if request.method == 'POST':
        data_to_save = data_manager.ANSWERS

        if answer_id:
            data_to_save[int(answer_id)]['message'] = request.form['answer_m']
            data_to_save[int(answer_id)]['submission_time'] = int(time.time())
        else:
            data_to_save.append({'id': util.find_next_id(data_to_save),
                                 'submission_time': int(time.time()),
                                 'vote_number': 0,
                                 'question_id': question_id,
                                 'message': request.form['answer_m']
                                 })

        connection.save_file(data_to_save, data_manager.ANSWERS_FILE_PATH)

        return redirect('/questions/' + question_id)

    if answer_id:
        answer_message = data_manager.ANSWERS[int(answer_id)]['message']

    return render_template('answer.html', answer_id=answer_id, answer_message=answer_message)

@app.route("/add", methods=['GET', 'POST'])
@app.route("/add/<question_id>", methods=['GET', 'POST'])
def add_question(question_message=None, question_id=None, title_m=None):




    if request.method == 'POST':
        data_to_save = data_manager.QUESTIONS

        if not question_id:
            question_title = request.form['title_m']
            print(question_id)
            question_id = (util.generete_new_id(data_manager.QUESTIONS))
            print(question_id)
            print(data_manager.QUESTIONS)
            data_to_save.append({'id': int(question_id),
                                 'submission_time': int(time.time()),
                                 'view_number': 0,
                                 'vote_number': 0,
                                 'message': request.form['question_m'],
                                 'title': request.form['title_m']
                                 })
        else:

            data_to_save[int(question_id)]['message'] = request.form['question_m']
            data_to_save[int(question_id)]['submission_time'] = int(time.time())
            data_to_save[int(question_id)]['title'] = request.form['title_m']
        print("doszlo tu")
        connection.save_file(data_to_save, data_manager.QUESTION_FILE_PATH)

        return redirect('/list')
    else:
        question_id = util.generete_new_id(data_manager.QUESTIONS)





    return render_template('note.html', question_id=question_id, question_message=question_message )




if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )
