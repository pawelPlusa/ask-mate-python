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
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def start():
    sorted_questions = sorted(data_manager.get_all_from_given_table("question"),
                              key=lambda i: i['submission_time'], reverse=1)

    return render_template("index.html", sorted_questions=util.change_time_format(sorted_questions),
                           headers=list(sorted_questions[0].keys())[1:])


@app.route("/delete/<question_id>")
@app.route("/delete/<question_id>/<int:confirmation>")
@app.route("/delete/answer/<question_id>/<answer_id>")
@app.route("/delete/answer/<question_id>/<answer_id>/<int:confirmation>")
def delete(question_id, confirmation=None, answer_id=None, status=None, question_tag_id=None):

    if confirmation:
        if answer_id:
            answer_sql_conditional = { "id" : int(answer_id)}
            data_manager.delete_data_in_table("answer", answer_sql_conditional)
        elif question_tag_id:
            pass

        else:
            answers_id_with_q_id = data_manager.get_from_table_condition("answer", {"question_id" : question_id}, "id")
            for single_answer_id in answers_id_with_q_id:
                 data_manager.delete_data_in_table("comment", single_answer_id)
            data_manager.delete_data_in_table("comment", {"question_id" : int(question_id)})
            data_manager.delete_data_in_table("answer", {"question_id" : int(question_id)})
            data_manager.delete_data_in_table("question_tag", {"question_id" : int(question_id)})
            data_manager.delete_data_in_table("question", {"id" : int(question_id)} )

        status = True

    return render_template("delete.html", question_id=question_id, answer_id=answer_id, status=status)


@app.route("/list")
@app.route("/list/<question_id>/<vote>")
def show_questions_list(question_id=None, vote=None, table="question"):

    question_list = data_manager.get_all_from_given_table(table)
    sorted_question_list = sorted(question_list, key=lambda i: i['submission_time'], reverse=1)

    if vote:
        util.check_if_vote(table, question_list, question_id, vote)
        return redirect("/list", code=303)
    return render_template("list.html", sorted_questions=util.change_time_format(sorted_question_list))


@app.route("/search")
def search_for_questions():
    message = title = ("%"+request.args.get("sphrase")+"%").lower()
    question_id_from_answers = data_manager.get_from_table_condition_like("answer", {"message" : message}, "question_id AS id")
    question_id_from_questions = data_manager.get_from_table_condition_like("question", {"message" : message, "title" : title}, "id")
    all_question_id = question_id_from_questions + question_id_from_answers

    if all_question_id:
        search_result = []
        for one_question_id in all_question_id:
            search_result.append(data_manager.get_from_table_condition("question",one_question_id)[0])
        return render_template("/list.html", sorted_questions=util.change_time_format(search_result))
    else:

        return render_template("/list.html", message="There is no record matching your criteria")

@app.route("/list/<sorted_by>/<int:direction>")
def show_questions(sorted_by,direction, table="question"):

    question_list = data_manager.get_all_from_given_table(table)
    sorted_questions = sorted(question_list, key=lambda i: i[sorted_by], reverse=direction)

    if sorted_by in ["submission_time", "vote_number", "view_number"]:
        sorted_questions.sort(key=lambda item: (item[sorted_by]), reverse=direction)
    elif sorted_by:
        sorted_questions.sort(key=lambda item: item[sorted_by], reverse=direction)

    return render_template("list.html",
                           sorted_questions=util.change_time_format(sorted_questions),
                           direction=direction)


@app.route("/questions/<question_id>")
def show_question(question_id):
    given_question = data_manager.get_from_table_condition("question", {"id": question_id})[0]
    answers = sorted(data_manager.get_from_table_condition("answer", {"question_id": question_id}),
                     key=lambda i: i["submission_time"], reverse=True)
    view_counter = given_question["view_number"] + 1
    data_manager.update_data_in_table("question", {"view_number" : view_counter}, {"id" : question_id})
    question_title = given_question["title"]
    question_message = given_question["message"]

    return render_template('questions.html',
                           question_id=question_id, question_title=question_title,
                           question_message=question_message, answers=util.change_time_format(answers))
@app.route("/questions/<question_id>/<sorted_by>/<int:direction>")
@app.route("/questions/vote/<question_id>/<answer_id>/<vote>")
def show_answers(question_id, answer_id=None, vote=None, sorted_by=None, direction=0):

    # if not answer_id and vote:



    # given_question = util.get_single_row(data_manager.get_all_from_given_table("question"), int(question_id)) # TODO: what for? is it not easier to SELECT single row FROM table?
    given_question = data_manager.get_from_table_condition("question", {"id": question_id})[0]

    answers = sorted(data_manager.get_from_table_condition("answer", {"question_id": question_id}),
                     key=lambda i: i["submission_time"], reverse=True)
    question_title = given_question["title"]
    question_message = given_question["message"]

    if vote:
        util.check_if_vote("answer", answers, answer_id, vote)
        return redirect("/questions/" + question_id, code=303)

    if sorted_by in ["submission_time", "vote_number"]:
        answers.sort(key=lambda item: (item[sorted_by]), reverse=direction)
    elif sorted_by:
        answers.sort(key=lambda item: item[sorted_by], reverse=direction)

    return render_template('questions.html',
                           question_id=question_id, question_title=question_title,
                           question_message=question_message, answers=util.change_time_format(answers) ,
                           direction=direction)


@app.route("/answer/<question_id>", methods=['GET', 'POST'])
@app.route("/answer/<question_id>/<answer_id>", methods=['GET', 'POST'])
def add_answer(question_id, answer_id=None, answer_message=None):

    # given_question = util.get_single_row(data_manager.get_all_from_given_table("question"), question_id)  # TODO: what for? is it not easier to SELECT single row FROM table?
    given_question = data_manager.get_from_table_condition("question", {"id" : question_id})[0]
    question_title = given_question["title"]

    if request.method == 'POST':
        if answer_id:
            data_to_save = {"message": request.form['answer_m'],
                            'submission_time': datetime.now()}
            data_manager.update_data_in_table("answer", data_to_save, {"id": answer_id})
        else:
            data_to_save = ({'submission_time':  datetime.now(),
                             'vote_number': '0',
                             'question_id': question_id,
                             'message': request.form['answer_m']
                            })

            data_manager.insert_data_to_table("answer", data_to_save)

        return redirect('/questions/' + question_id)

    if answer_id:
        answer_message = data_manager.get_from_table_condition("answer", {"id": answer_id})[0]["message"]

    return render_template('answer.html',
                           answer_id=answer_id, answer_message=answer_message,
                           question_title=question_title)


@app.route("/note", methods=['GET', 'POST'])
@app.route("/note/<question_id>", methods=['GET', 'POST'])
def add_question(message=None, title=None, question_id=None, table="question"):

    if request.method == 'GET' and question_id:
        single_row = util.get_single_row(data_manager.get_all_from_given_table(table), int(question_id))  # TODO: what for? is it not easier to SELECT single row FROM table?
        title = single_row["title"]
        message = single_row["message"]
    elif request.method == 'POST':
        if not question_id:
            data_to_save = {'submission_time': datetime.now(),
                            'view_number': 0,
                            'vote_number': 0,
                            'message': request.form['question_m'].capitalize(),
                            'title': request.form['title_m'].capitalize(),
                            'image': None
                            }

            data_manager.insert_data_to_table(table, data_to_save)
        else:
            data_to_save = {'message': request.form['question_m'].capitalize(),
                            'submission_time': datetime.now(),
                            'title': request.form['title_m'].capitalize()
                            }

            sql_conditions = {'id': question_id}
            data_manager.update_data_in_table(table, data_to_save, sql_conditions)

        return redirect('/list')

    return render_template('note.html', message=message, title=title, question_id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=6969
    )
