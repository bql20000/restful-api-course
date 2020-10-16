from user import User

users = [
    User(3, 'bob', 'asdf')
]


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    print(type(payload))
    print(payload)
    user_id = payload['identity']
    return User.find_by_id(user_id)


