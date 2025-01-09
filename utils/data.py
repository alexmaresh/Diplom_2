from utils.user import User


class DataUser(User):

    params_exist = {
        "email": "test-data@yandex.ru",
        "password": "password",
        "name": "Username",
    }
    @staticmethod
    def get_data():
        return User.generate_user_data()





