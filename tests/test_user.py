import pytest
import requests
import allure

from routes import BurgerRoutes as r
from error_messages import ErrorMessages as e


@allure.feature("Метод создания юзера")
class TestCreateUser:
    @allure.title("Успешное создание юзера")
    def test_create_user_success(self, user_data):
        url = r.REGISTER
        resp = requests.post(url, json=user_data)
        assert resp.status_code == 200 and resp.json()['accessToken']

    @allure.title("Неуспешное создание юзера с уже существующими параметрами")
    def test_create_existing_user_fail(self):
        url = r.REGISTER
        params = {
            "email": "test-data@yandex.ru",
            "password": "password",
            "name": "Username"
        }
        resp = requests.post(url, json=params)
        assert resp.status_code == 403, resp.json() and resp.json()['message'] == e.user_exists and resp.json()[
            'success'] == False

    @pytest.mark.parametrize(
        "field", ["email", "password", "name"]
    )
    @allure.title("Неуспешное создание юзера без обязательных полей")
    def test_create_user_without_required_field_fail(self, field, user_data):
        user_data[field] = ''
        url = r.REGISTER
        resp = requests.post(url, json=user_data)
        assert resp.status_code == 403, resp.json() and resp.json()['message'] == e.required_fields and resp.json()[
            'success'] == False

@allure.feature("Метод авторизации юзера")
class TestLoginUser:
    @allure.title("Успешный логин юзера")
    def test_login_user_success(self, created_user):
        resp = requests.post(r.LOGIN, json=created_user)
        assert resp.status_code == 200 and resp.json()['user']['email'] == created_user['email'], resp.json()

    @pytest.mark.parametrize(
        "field", ["email", "password"]
    )
    @allure.title("Неуспешный логин юзера с неверным логином или паролем")
    def test_login_user_fail(self, created_user, field):
        created_user[field] = ''
        resp = requests.post(r.LOGIN, json=created_user)
        assert resp.status_code == 401 and resp.json()['message'] == e.incorrect_fields

@allure.feature("Метод изменения данных юзера")
class TestChangeUserData:

    @pytest.mark.parametrize(
        "field", ["email", "name"]
    )
    @allure.title('Проверка изменения логина и емейла авторизованного юзера')
    def test_change_data_user_authorized(self, logined_user, field):
        user_data, token = logined_user
        user_data[field] = 'changed_' + str(user_data[field])
        change_info = requests.patch(r.USER, json=user_data, headers={'Authorization': token})
        assert change_info.status_code == 200 and change_info.json()['user'][field] == user_data[field], change_info.resp()

    @pytest.mark.parametrize(
        "field", ["email", "name"]
    )
    @allure.title('Проверка изменения логина и емейла неавторизованного юзера')
    def test_change_data_user_unauthorized(self, logined_user, field):
        user_data, token = logined_user
        user_data[field] = 'changed_' + str(user_data[field])
        change_info = requests.patch(r.USER, json=user_data)
        assert change_info.status_code == 401 and change_info.json()['message'] == e.authorized

    @allure.title('Проверка изменения емейла авторизованного юзера на уже существуюший')
    def test_change_existed_email_user_authorized(self, logined_user):
        user_data, token = logined_user
        user_data['email'] = "test-data@yandex.ru"
        change_info = requests.patch(r.USER, json=user_data, headers={'Authorization': token})
        assert change_info.status_code == 403 and change_info.json()['message'] == e.email_exists