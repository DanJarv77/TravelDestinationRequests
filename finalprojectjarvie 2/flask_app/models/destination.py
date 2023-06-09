from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "destinations"
class Destination:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.what_happened = db_data['what_happened']
        self.date_travel = db_data['date_travel']
        self.number_group = db_data['number_group']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM destinations
                JOIN users on destinations.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        destinations = []
        for row in results:
            this_destination = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_destination.creator = user.User(user_data)
            destinations.append(this_destination)
        return destinations
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM destinations
                JOIN users on destinations.user_id = users.id
                WHERE destinations.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_destination = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_destination.creator = user.User(user_data)
        return this_destination

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO destinations (location,what_happened,date_travel,number_group,user_id)
                VALUES (%(location)s,%(what_happened)s,%(date_travel)s,%(number_group)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE destinations
                SET location = %(location)s,
                what_happened = %(what_happened)s,
                date_travel = %(date_travel)s ,
                number_group = %(number_group)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM destinations
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_destination(form_data):
        is_valid = True

        if len(form_data['location']) < 2:
            flash("All Fields Required")
            is_valid = False
        if len(form_data['what_happened']) < 2:
            flash("ALl Fields Required")
            is_valid = False
        if form_data['date_travel'] == '':
            flash("Please input a date.")
            is_valid = False
        if (form_data['number_group']) == '':
            flash("Must have at least 1 or more to start group")
            is_valid = False

        return is_valid