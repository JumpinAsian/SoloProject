from flask_app.config.mysqlconnection import connect
from flask_app.models import user
from flask import flash
mydb = "projectLog"


class Project:
    def __init__(self, data):
        self.id = data['id']
        self.project_name = data['project_name']
        self.client_name = data['client_name']
        self.word_count = data['word_count']
        self.word_rate = data['word_rate']
        self.amount_total = data['amount_total']
        self.start_date = data['start_date']
        self.due_date = data['due_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO projects (project_name, client_name, word_count, word_rate, amount_total, start_date, due_date, user_id)
                VALUES (%(project_name)s,%(client_name)s,%(word_count)s,%(word_rate)s,%(amount_total)s,%(start_date)s,%(due_date)s,%(user_id)s);
                """
        return connect(mydb).query_db(query, data)

    @classmethod
    def get_all_projects(cls):
        query = """
                SELECT * FROM projects
                JOIN users on projects.user_id = users.id;
                """
        results = connect(mydb).query_db(query)
        projects = []
        for row in results:
            this_project = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_project.creator = user.User(user_data)
            projects.append(this_project)
        return projects

    @classmethod
    def get_project_by_id(cls, data):
        query = """
                SELECT * FROM projects
                JOIN users on projects.user_id = users.id
                WHERE projects.id = %(id)s;
                """
        result = connect(mydb).query_db(query, data)
        # print('results', result)
        if not result:
            return False
        result = result[0]
        this_project = cls(result)
        user_data = {
            "id": result['users.id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": "",
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at']
        }
        this_project.creator = user.User(user_data)
        # print('this_project', this_project)
        return this_project

    @classmethod
    def update_project(cls, form_data):
        query = """
                UPDATE projects
                SET project_name = %(project_name)s,
                client_name = %(client_name)s,
                word_count = %(word_count)s,
                word_rate = %(word_rate)s,
                amount_total = %(amount_total)s,
                start_date = %(start_date)s,
                due_date = %(due_date)s,
                WHERE id = %(id)s;
                """
        results = connect(mydb).query_db(query, form_data)
        print(results)
        return results

    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM projects
                WHERE id = %(id)s;
                """
        return connect(mydb).query_db(query, data)

    @staticmethod
    def validate_project(request):
        is_valid = True
        if len(request['project_name']) < 1:
            is_valid = False
            flash('*Project Name required')
        elif len(request['project_name']) <= 1:
            is_valid = False
            flash('*Project Name must be at least 2 characters long')
        if len(request['client_name']) < 1:
            is_valid = False
            flash('*Client Name required')
        elif len(request['client_name']) <= 1:
            is_valid = False
            flash('*Client Name must be at least 2 characters long')
        if len(request['word_count']) < 1:
            is_valid = False
            flash('*Word Count Required')
        if len(request['word_rate']) < 0:
            is_valid = False
            flash('*Word Rate Required')
        # if len(request['home_city']) < 1:
        #     is_valid = False
        #     flash('*Home City required')
        # elif len(request['home_city']) <= 1:
        #     is_valid = False
        #     flash('*Home City must be at least 2 characters long')
        return is_valid
