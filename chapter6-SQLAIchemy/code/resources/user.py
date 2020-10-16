import sqlite3
from flask_restful import reqparse, Resource


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
