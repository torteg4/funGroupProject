from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, card

@app.route("/dashboard")
def all_cards_page():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", this_user= user.User.get_user_by_id(data))


# route that will show the new card page
@app.route("/new/card")
def new_card():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("/create_card.html", this_user = user.User.get_user_by_id(data))

# shows a specific card
@app.route("/show/<int:id>")
def view_card(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    dict = {
        "id": session["user_id"]
    }
    return render_template("/view_card.html", this_user = user.User.get_user_by_id(dict), this_card = card.Card.get_one_card(data))

# route that will show a card to edit
@app.route("/edit/<int:id>")
def edit_card(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    return render_template("/edit_card.html", this_card = card.Card.get_one_card(data))

# deletes card from database
@app.route("/cards/delete/<int:id>")
def delete_card(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    Card.delete_card(data)
    return redirect("/dashboard")

# add a card to database
@app.route("/cards/add_to_db", methods=["POST"])
def add_card_to_db():
    if "user_id" not in session:
        return redirect("/")
    if not card.Card.validate_card(request.form):
        return redirect("/new/card")

    data = {
        "name": request.form["name"],
        "bio": request.form["bio"],
        "skills": request.form["skills"],
        "stats": request.form["stats"],
        "user_id": session["user_id"],
    }
    card.Card.add_card(data)
    return redirect("/dashboard")

# edit a card in the database
@app.route("/cards/edit_in_db/<int:id>", methods=["POST"])
def edit_card_in_db(id):
    if "user_id" not in session:
        return redirect("/")
    if not Card.validate_card(request.form):
        return redirect(f"/edit/{id}")

    data = {
        "name": request.form["name"],
        "bio": request.form["bio"],
        "skills": request.form["skills"],
        "stats": request.form["stats"],
        "id": id,
    }
    card.Card.edit_card(data)
    return redirect("/dashboard")