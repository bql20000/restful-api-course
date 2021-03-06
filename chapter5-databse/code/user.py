import sqlite3
from flask_restful import request, reqparse, Resource


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        user = cls(*row) if row else None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        user = cls(*row) if row else None
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
    )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        # data = request.get_json()

        if User.find_by_username(data['username']):
            return {"message": "Sorry, username existed."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Bad!!!
        # username_query = "SELECT * FROM users WHERE username=?"
        # if cursor.execute(username_query, (data['username'],)):
        #     return {"message": "Sorry, username existed."}


        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(insert_query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
