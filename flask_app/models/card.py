from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Card:
    db_name = "not_a_scam_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.bio = data["bio"]
        self.skills = data["skills"]
        self.stats = data["stats"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @classmethod
    def add_card(cls, data):
        query = """
        INSERT INTO cards
        (name, bio, skills, stats, user_id)
        VALUES
        (%(name)s, %(bio)s, %(skills)s, %(stats)s, %(user_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_cards(cls):
        query = """
        SELECT * FROM cards
        JOIN users
        ON cards.user_id = users.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        if len(results) == 0:
            return []
        else:
            all_card_objects = []
            for card_dictionary in results:
                card_obj = cls(card_dictionary)
                # Grab the user's info
                user_dictionary = {
                    "id": card_dictionary["users.id"],
                    "first_name": card_dictionary["first_name"],
                    "last_name": card_dictionary["last_name"],
                    "tier": card_dictionary["tier"],
                    "email": card_dictionary["email"],
                    "password": card_dictionary["password"],
                    "created_at": card_dictionary["users.created_at"],
                    "updated_at": card_dictionary["users.updated_at"]
                }
                # Create the User object
                user_obj = user.User(user_dictionary)
                # Link this User to this card
                card_obj.user = user_obj
                # Add this card to the list of all card objects
                all_card_objects.append(card_obj)
            return all_card_objects

    @classmethod
    def get_one_card(cls, data):
        query = """
        SELECT * FROM cards
        JOIN users 
        ON cards.user_id = users.id
        WHERE cards.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            # create a variable for results[index] for clarity
            card_dictionary = results[0]
            card_obj = cls(card_dictionary)
            # Grab the user's info
            user_dictionary = {
                "id": card_dictionary["users.id"],
                "first_name": card_dictionary["first_name"],
                "last_name": card_dictionary["last_name"],
                "email": card_dictionary["email"],
                "password": card_dictionary["password"],
                "created_at": card_dictionary["users.created_at"],
                "updated_at": card_dictionary["users.updated_at"]
            }
            # Create the User object
            user_obj = user.User(user_dictionary)
            # Link this User to this card
            card_obj.user = user_obj
        return card_obj

    @classmethod
    def edit_card(cls, data):
        query= """
        UPDATE cards SET
        name = %(name)s,
        race = %(bio)s,
        classname = %(skills)s,
        level = %(stats)s
        WHERE
        id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_card(cls, data):
        query= "DELETE FROM cards WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_card(form_data):
        is_valid = True
        if len(form_data["name"]) < 2:
            flash ("Name must be 2 or more cards")
            is_valid = False
        if len(form_data["bio"]) < 2:
            flash ("Bio must be 2 or more cards")
            is_valid = False
        if len(form_data["skills"]) < 2:
            flash ("Skills must be 2 or more cards")
            is_valid = False
        if len(form_data["stats"]) < 1:
            flash ("Stats must be between 1 and 100")
            is_valid = False
        return is_valid