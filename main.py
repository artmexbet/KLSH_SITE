from flask import Flask, render_template, request, redirect, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from data import db_session
from data.users import User
from data.roles import Roles
from data.teams import Teams
from data.competitions import Competitions
from data.achievements import Achievements
from data.punishments import Punishments

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'klsh_secret_key'

ADMIN_ID = 3


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def main_page():
    return render_template("main.html", title="Главная")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html", title="Вход")
    form = request.form
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == form["login"]).first()
    if user and user.check_password(form["password"]):
        login_user(user, remember=bool(form.get("remember_me", False)))
        return redirect("/")
    else:
        return render_template("login.html", error="Неверный логин или пароль", title="Вход")


@login_required
@app.route("/register", methods=["GET", "POST"])
def register():
    if not current_user.is_authenticated or current_user.role.title != "Админ":
        return abort(404)
    db_sess = db_session.create_session()
    if request.method == "GET":
        return render_template("register_form.html",
                               roles=db_sess.query(Roles).all(),
                               teams=db_sess.query(Teams).all())

    form = request.form
    user = User()
    user.login = form['login']
    user.name = form['name']
    user.set_password(form["password"])
    user.role_id = db_sess.query(Roles).filter(Roles.title == form["role"]).first().id
    user.team_id = db_sess.query(Teams).filter(Teams.title == form["team"]).first().id
    user.year = int(form["year"])

    db_sess.add(user)
    db_sess.commit()

    return redirect("/register")


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route("/students")
def students_page():
    db_sess = db_session.create_session()
    if current_user.role.title == "Админ":
        return render_template("student_info.html",
                               students=db_sess.query(User).filter(
                                   User.role_id != ADMIN_ID))
    elif current_user.role.title == "Школьник":
        return render_template("student_info.html", students=[current_user])
    else:
        abort(404)


@login_required
@app.route("/students/<int:student_id>")
def get_student(student_id):
    db_sess = db_session.create_session()
    if current_user.role.title == "Админ":
        user = db_sess.query(User).get(student_id)
    elif current_user.id != student_id:
        user = None
    else:
        user = db_sess.query(User).get(current_user.id)
    if user:
        return render_template("a_student_info.html", student=user)
    else:
        abort(404)


# TODO: добавление и удаление нарядов и достижений, добавление соревнований

@app.route("/teams")
def get_teams():
    return render_template("teams.html", teams=db_session.create_session().query(Teams).all())


@login_required
@app.route("/teams/add", method=["POST", "GET"])
def add_team():
    if current_user.role.title != "Админ":
        abort(404)
    if request.method == "GET":
        return render_template("add_team.html")
    form = request.form
    db_sess = db_session.create_session()
    team = Teams()
    team.title = form["title"]
    db_sess.add(team)
    db_sess.commit()
    return redirect("/teams")


@app.route("/competitions")
def get_competitions_list():
    db_sess = db_session.create_session()
    return render_template("competitions.html", competitions=db_sess.query(Competitions).all())


@app.route("/competitions/add", methods=["POST", "GET"])
@login_required
def add_competition():
    if current_user.role.title != "Админ":
        abort(404)
    if request.method == "GET":
        return render_template("add_competition.html")


if __name__ == "__main__":
    db_session.global_init("db/klsh_db.db")
    app.run(debug=True)
