from flask_restful import reqparse, Resource
from models.user import UserModel

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

        if UserModel.find_by_username(data['username']):
            return {"message": "Sorry, username existed."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
