from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models import card

class User:
    db_name = "not_a_scam_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        # self.tier = data["tier"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.cards = []

    @classmethod
    def register_user(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
        
    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

    @classmethod
    def get_users_card(cls, data):
        query = """
        SELECT * FROM users
        LEFT JOIN cards
        ON users.id = cards.user_id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            user_obj = cls(results[0])
            for user_card in results:
                card_dictionary = {
                    "id": user_card["cards.id"],
                    "name": user_card["name"],
                    "bio": user_card["bio"],
                    "skills": user_card["skills"],
                    "stats": user_card["stats"],
                    "created_at": user_card["cards.created_at"],
                    "updated_at": user_card["cards.updated_at"]
                }
                card_obj = card.Card(card_dictionary)
                user_obj.cards.append(card_obj)
            return user_obj
    
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 2:
            flash("First name must be 2 or more characters", "register")
            is_valid = False
        if len(form_data["last_name"]) < 2:
            flash("Last name must be 2 or more characters", "register")
            is_valid = False
        # if len(form_data["tier"]) < 2:
        #     flash("Tier must be 2 or more characters", "register")
        #     is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        data = {
            "email": form_data["email"]
        }
        found_user_or_none = User.get_user_by_email(data)
        if found_user_or_none != None:
            flash("Email already taken", "register")
            is_valid = False
        if len(form_data["password"]) < 8:
            flash("Password must be 8 or more characters", "register")
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid login credentials", "login")
            return False
        data = {
            "email": form_data["email"]
        }
        found_user_or_none = User.get_user_by_email(data)
        if found_user_or_none == None:
            flash("Invalid login credentials", "login")
            return False
        if not bcrypt.check_password_hash(found_user_or_none.password, form_data["password"]):
            flash("Invalid login credentials", "login")
            return False

        return found_user_or_none