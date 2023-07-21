from flask_app.config.mysqlconnection import connect
from flask import flash
from flask_app import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mydb = 'projectLog'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, request):
        hashed_data = {
            'first_name': request['first_name'],
            'last_name': request['last_name'],
            'email': request['email'],
            'password': bcrypt.generate_password_hash(request['password']),
        }
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        #  "return connect(mydb).query_db(query, hashed_data)"
        user_data = connect(mydb).query_db(query, hashed_data)
        print(user_data)
        return user_data

    @classmethod
    def get_user_by_email(cls, data):
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s;
                """
        result = connect(mydb).query_db(query, data)
        print(result)
        #  if not result:
        #  return False
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = """
                SELECT * FROM users
                WHERE users.id = %(id)s;
                """
        result = connect(mydb).query_db(query, data)
        print(result)
        if not result:
            return False
        this_user = cls(result[0])
        print(this_user)
        return this_user

    @classmethod
    def get_all_users(cls):
        query = """
                SELECT *
                FROM users;
                """
        results = connect(mydb).query_db(query)
        # print(results)
        output = []
        for user_dictionary in results:
            output.append(cls(user_dictionary))
        return output

    @staticmethod
    def validate_reg(request):
        is_valid = True
        if len(request['first_name']) < 1:
            is_valid = False
            flash('*First Name required', 'regError')
        elif len(request['first_name']) <= 1:
            is_valid = False
            flash('*First Name must be at least 2 characters long', 'regError')
        if len(request['last_name']) < 1:
            is_valid = False
            flash('*Last Name required', 'regError')
        elif len(request['last_name']) <= 1:
            is_valid = False
            flash('*Last Name must be at least 2 characters long', 'regError')
        if len(request['email']) < 1:
            is_valid = False
            flash('*Email required', 'regError')
        elif not EMAIL_REGEX.match(request['email']):
            is_valid = False
            flash('*Email invalid', 'regError')
        if len(request['password']) < 8:
            is_valid = False
            flash('*Password must be at least 8 characters long', 'regError')
        elif request['password'] != request['confirm_password']:
            is_valid = False
            flash('*Passwords must match', 'regError')
        if User.get_user_by_email(request):
            is_valid = False
            flash('*Email already exists', 'regError')
        return is_valid

    @staticmethod
    def validate_login(request):
        if not EMAIL_REGEX.match(request['email']):
            flash("Invalid email/password.", "logError")
            return False
        this_user = User.get_user_by_email(request)
        if not this_user:
            flash("Invalid email/password.", "logError")
            return False
        if not bcrypt.check_password_hash(this_user.password, request['password']):
            flash("Invalid email/password.", "logError")
            return False
        return this_user
