from flask import Flask, render_template, request, redirect, escape, session, url_for
import data_manager
import util
import psycopg2
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#2211aay2L"F4Q8z\n\xec]/'


@app.route("/")
def start():
    questions = data_manager.get_question_data_with_username()
    print(questions)
    print(session)
    if questions:
        sorted_questions = sorted(questions, key=lambda i: i['submission_time'], reverse=1)
        return render_template("index.html", sorted_questions=util.change_time_format(sorted_questions),
                               headers=list(sorted_questions[0].keys())[1:],
                               session=session
                               )

    else:
        return render_template("index.html", sorted_questions=None, headers=None,
                               session=escape(session["username"]) if 'username' in session else 0)


@app.route("/delete/<question_id>")
@app.route("/delete/<question_id>/<int:confirmation>")
@app.route("/delete/answer/<question_id>/<answer_id>")
@app.route("/delete/answer/<question_id>/<answer_id>/<int:confirmation>")
def delete(question_id, confirmation=None, answer_id=None, status=None, question_tag_id=None):

    if "username" not in session:
        return render_template("redirect.html",
                               why_redirected_text="You are not logged in",
                               where_redirect="log_in", time=2)

    if confirmation:
        if answer_id:
            answer_sql_conditional = {"id": int(answer_id)}
            data_manager.delete_data_in_table("answer", answer_sql_conditional)
        elif question_tag_id:
            pass

        else:

            data_manager.delete_data_in_table("question", {"id": int(question_id)})

        status = True

    return render_template("delete.html", question_id=question_id, answer_id=answer_id, status=status, session=session)


@app.route("/list")
@app.route("/list/<question_id>/<vote>")
def show_questions_list(question_id=None, vote=None, table="question"):

    question_list = data_manager.get_all_from_given_table(table)
    sorted_question_list = sorted(question_list, key=lambda i: i['submission_time'], reverse=1)

    if vote:
        if "username" not in session:
            return render_template("redirect.html", why_redirected_text="You are not logged in",
                                   where_redirect="log_in", time=2)

        util.check_if_vote(table, question_id, vote)
        return redirect("/vote_given", code=303)

    return render_template("list.html",
                           sorted_questions=util.change_time_format(sorted_question_list),
                           session=session)


@app.route("/search")
def search_for_questions():
    message = title = ("%"+request.args.get("sphrase")+"%").lower()
    question_id_from_answers = data_manager.get_from_table_condition_like(
        "answer", {"message": message}, "question_id AS id")
    question_id_from_questions = data_manager.get_from_table_condition_like(
        "question", {"message": message, "title": title}, "id")
    all_question_id = question_id_from_questions + question_id_from_answers

    if all_question_id:
        search_result = []
        for one_question_id in all_question_id:
            search_result.append(data_manager.get_from_table_condition("question", one_question_id)[0])
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
                           direction=direction, session=session)


@app.route("/questions/<question_id>")
def show_question(question_id):
    given_question = data_manager.get_from_table_condition("question", {"id": question_id})[0]
    answers = sorted(data_manager.get_from_table_condition("answer", {"question_id": question_id}),
                     key=lambda i: i["submission_time"], reverse=True)
    data_manager.update_data_in_table("question",
                                      {"view_number": (given_question["view_number"] + 1)}, {"id": question_id})
    question_title = given_question["title"]
    question_message = given_question["message"]

    return render_template('questions.html',
                           question_id=question_id, question_title=question_title,
                           question_message=question_message, answers=util.change_time_format(answers),
                           session=session)


@app.route("/questions/<question_id>/<sorted_by>/<int:direction>")
@app.route("/questions/vote/<question_id>/<answer_id>/<vote>")
def show_answers(question_id, answer_id=None, vote=None, sorted_by=None, direction=0):

    given_question = data_manager.get_from_table_condition("question", {"id": question_id})[0]
    answers = sorted(data_manager.get_from_table_condition("answer", {"question_id": question_id}),
                     key=lambda i: i["submission_time"], reverse=True)
    question_title = given_question["title"]
    question_message = given_question["message"]

    if vote:
        if "username" not in session:
            return render_template("redirect.html", why_redirected_text="You are not logged in",
                                   where_redirect="log_in", time=2)
        util.check_if_vote("answer", answer_id, vote)
        return redirect("/vote_given/"+question_id, code=303)

    if sorted_by in ["submission_time", "vote_number"]:
        answers.sort(key=lambda item: (item[sorted_by]), reverse=direction)
    elif sorted_by:
        answers.sort(key=lambda item: item[sorted_by], reverse=direction)

    return render_template('questions.html',
                           question_id=question_id, question_title=question_title,
                           question_message=question_message, answers=util.change_time_format(answers) ,
                           direction=direction, session=session)


@app.route("/answer/<question_id>", methods=['GET', 'POST'])
@app.route("/answer/<question_id>/<answer_id>", methods=['GET', 'POST'])
def add_answer(question_id, answer_id=None, answer_message=None):

    if "username" not in session:
        return render_template("redirect.html", why_redirected_text="You are not logged in",
                               where_redirect="log_in", time=2)

    given_question = data_manager.get_from_table_condition("question", {"id": question_id})[0]
    question_title = given_question["title"]

    if request.method == 'POST':
        if answer_id:
            data_to_save = {"message": util.proper_capitalization(request.form['answer_m']),
                            'submission_time': datetime.now()}
            data_manager.update_data_in_table("answer", data_to_save, {"id": answer_id})
        else:
            data_to_save = ({'submission_time':  datetime.now(),
                             'vote_number': '0',
                             'question_id': question_id,
                             'message': util.proper_capitalization(request.form['answer_m']),
                             'user_id': session["user_id"]
                             })

            data_manager.insert_data_to_table("answer", data_to_save)

        return redirect('/questions/' + question_id)

    if answer_id:
        answer_message = data_manager.get_from_table_condition("answer", {"id": answer_id})[0]["message"]

    return render_template('answer.html',
                           answer_id=answer_id, answer_message=answer_message,
                           question_title=question_title, session=session)


@app.route("/note", methods=['GET', 'POST'])
@app.route("/note/<question_id>", methods=['GET', 'POST'])
def add_question(message=None, title=None, question_id=None, table="question"):

    if "username" not in session:
        return render_template("redirect.html", why_redirected_text="You are not logged in",
                               where_redirect="log_in", time=2)

    if request.method == 'GET' and question_id:
        single_row = data_manager.get_from_table_condition("question", {"id" : question_id})[0]
        title = single_row["title"]
        message = single_row["message"]
    elif request.method == 'POST':
        if not question_id:
            data_to_save = {'submission_time': datetime.now(),
                            'view_number': 0,
                            'vote_number': 0,
                            'message': util.proper_capitalization(request.form['question_m']),
                            'title': util.proper_capitalization(request.form['title_m']),
                            'image': None,
                            'user_id': session["user_id"]
                            }

            data_manager.insert_data_to_table(table, data_to_save)
        else:
            data_to_save = {'message': util.proper_capitalization(request.form['question_m']),
                            'submission_time': datetime.now(),
                            'title': util.proper_capitalization(request.form['title_m'])
                            }

            sql_conditions = {'id': question_id}
            data_manager.update_data_in_table(table, data_to_save, sql_conditions)

        return redirect('/list')

    return render_template('note.html', message=message, title=title, question_id=question_id, session=session)


@app.route("/vote_given/<int:question_id>")
@app.route("/vote_given")
def thank_you(question_id=None):
    if question_id:
        return render_template("vote_given.html", question_id=question_id)
    else:
        return render_template("vote_given.html")


@app.route("/registration", methods=["GET", "POST"])
def user_registration():

    if request.method == "GET":
        return render_template("registration.html")
    else:
        data_to_insert = {
            "login": request.form["email"],
            "password": util.hash_password(request.form["userpass"]),
            "user_name": request.form["username"],
            "registration_date": datetime.now()
        }

        try:
            data_manager.insert_data_to_table("users", data_to_insert)
        except psycopg2.errors.UniqueViolation:
            return (render_template("redirect.html",
                                    why_redirected_text="Registration fail (user with given e-mail already exists)",
                                    time=4))

        return render_template("redirect.html", why_redirected_text="Registration successful", time=2)


@app.route("/log_in", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":

        return render_template("login.html")

    else:
        user_data = data_manager.get_from_table_condition("users", {"login": request.form["email"]})

        if not user_data:
            return render_template("redirect.html", why_redirected_text="Wrong username or password",
                                    where_redirect="log_in", time=2)

        user_data = user_data[0]
        is_matching = util.verify_password(request.form["userpass"], user_data["password"])
        if is_matching:
            session['username'] = escape(user_data["user_name"])
            session["user_id"] = user_data["id"]

            return render_template("redirect.html", why_redirected_text="You are now logged in", time=2)
        return render_template("redirect.html", why_redirected_text="Wrong username or password", time=2)


@app.route("/log_out")
def user_logout():
    session.pop('username', None)
    return render_template("redirect.html", why_redirected_text="You have been logout", time=2)

@app.route("/users/<user_id>")
@app.route("/users")
def show_users(user_id=None):
    if "username"not in session:
        return render_template("redirect.html", why_redirected_text="You are not logged in",
                               where_redirect="log_in", time=2)
    if user_id:
        question_columns = "id, submission_time, view_number, vote_number, title, message"
        answer_columns = "id, question_id, submission_time, vote_number, message, accepted"
        comment_columns = "id, submission_time, message"
        all_single_user_data = {
        "single_user_data": util.change_time_format(data_manager.get_all_user_data(int(user_id)), "registration_date"),
        "single_user_questions": util.change_time_format(data_manager.get_from_table_condition(
                                "question", {"user_id":user_id}, question_columns)),
        "single_user_answers": util.change_time_format(data_manager.get_from_table_condition(
                                "answer", {"user_id":user_id}, answer_columns)),
        "single_user_comments": util.change_time_format(data_manager.get_from_table_condition(
                                "comment", {"user_id":user_id}, comment_columns))
        }

        return render_template("users.html", user_data=all_single_user_data)

    users_data = data_manager.get_all_user_data()
    headers = (list(users_data[0].keys()))
    return render_template("users.html", users_data=util.change_time_format(users_data, "registration_date"),
                           headers=headers)


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=6969
    )
