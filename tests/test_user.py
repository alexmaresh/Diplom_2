import pytest
import requests
import allure

from utils.routes import BurgerRoutes as BR
from utils.data import DataUser as DU
from utils.error_messages import ErrorMessages as e


@allure.feature("Метод создания юзера")
class TestCreateUser:
    @allure.title("Успешное создание юзера")
    def test_create_user_success(self, created_user):
        assert created_user["accessToken"]

    @allure.title("Неуспешное создание юзера с уже существующими параметрами")
    def test_create_existing_user_fail(self):
        url = BR.REGISTER
        params = DU.params_exist
        resp = requests.post(url, json=params)
        assert resp.status_code == 403 and resp.json()["message"] == e.user_exists

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Неуспешное создание юзера без обязательных полей")
    def test_create_user_without_required_field_fail(self, field):
        user = DU.get_data()
        user[field] = ""
        url = BR.REGISTER
        resp = requests.post(url, json=user)
        assert resp.status_code == 403 and resp.json()["message"] == e.required_fields


@allure.feature("Метод авторизации юзера")
class TestLoginUser:
    @allure.title("Успешный логин юзера")
    def test_login_user_success(self, created_user):
        resp = requests.post(BR.LOGIN, json=created_user)
        assert (
            resp.status_code == 200
            and resp.json()["user"]["email"] == created_user["email"]
        )

    @pytest.mark.parametrize("field", ["email", "password"])
    @allure.title("Неуспешный логин юзера с неверным логином или паролем")
    def test_login_user_fail(self, created_user, field):
        created_user[field] = ""
        resp = requests.post(BR.LOGIN, json=created_user)
        assert resp.status_code == 401 and resp.json()["message"] == e.incorrect_fields


@allure.feature("Метод изменения данных юзера")
class TestChangeUserData:
    @pytest.mark.parametrize("field", ["email", "name"])
    @allure.title("Проверка изменения логина и емейла авторизованного юзера")
    def test_change_data_user_authorized(self, logined_user, field):
        logined_user[field] = "changed_" + str(logined_user[field])
        change_info = requests.patch(
            BR.USER,
            json=logined_user,
            headers={"Authorization": logined_user["accessToken"]},
        )
        assert (
            change_info.status_code == 200
            and change_info.json()["user"][field] == logined_user[field]
        )

    @pytest.mark.parametrize("field", ["email", "name"])
    @allure.title("Проверка изменения логина и емейла неавторизованного юзера")
    def test_change_data_user_unauthorized(self, created_user, field):
        created_user[field] = "changed_" + str(created_user[field])
        change_info = requests.patch(BR.USER, json=created_user)
        assert (
            change_info.status_code == 401
            and change_info.json()["message"] == e.authorized
        )

    @allure.title("Проверка изменения емейла авторизованного юзера на уже существуюший")
    def test_change_existed_email_user_authorized(self, logined_user):
        logined_user["email"] = "test-data@yandex.ru"
        change_info = requests.patch(
            BR.USER,
            json=logined_user,
            headers={"Authorization": logined_user["accessToken"]},
        )
        assert (
            change_info.status_code == 403
            and change_info.json()["message"] == e.email_exists
        )
