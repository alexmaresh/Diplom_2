from faker import Faker
import allure
import requests
from routes import BurgerRoutes as r


class User:
    @staticmethod
    @allure.step("Генерация данных юзера")
    def generate_user_data():
        fake = Faker()
        payload = {
            "email": fake.email(),
            "password": fake.password(),
            "name": fake.first_name()
        }
        return payload

    @allure.step("Cоздание пользователя")
    def create_user(self):
        params = self.generate_user_data()
        resp = requests.post(r.REGISTER, json=params)
        return params, resp.json()

    @allure.step("Удаление пользователя")
    def delete_user(self, access_token):
        return requests.delete(r.USER, headers={'Authorization': access_token})

    @allure.step("Авторизация пользователя")
    def login_user(self, user_params):
        resp = requests.post(r.LOGIN, json=user_params)
        assert resp.status_code == 200
