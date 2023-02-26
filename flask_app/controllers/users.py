from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/user/cards")
def users_card():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("users_cards.html", this_users_cards = User.get_users_card(data))

@app.route("/register", methods=["POST"])
def register_user():
    if not User.validate_registration(request.form):
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    session["user_id"] = User.register_user(data)

    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def log_user_in():
    found_user_or_false = User.validate_login(request.form)
    if not found_user_or_false:
        return redirect("/")
    session["user_id"] = found_user_or_false.id
    return redirect("/dashboard")


@app.route("/logout")
def logout_user():
    session.clear()
    return redirect('/')