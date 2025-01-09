import pytest
import requests
import allure

from utils.routes import BurgerRoutes as BR
from utils.error_messages import ErrorMessages as e


@allure.feature("Метод создания заказа")
class TestCreateOrder:
    @allure.title("Успешное создание заказа c авторизацией и ингредиентами")
    @pytest.mark.parametrize("num", [2])
    def test_create_order_authorized_success(self, get_some_ingrs, logined_user):
        resp = requests.post(
            BR.ORDERS,
            json=get_some_ingrs,
            headers={"Authorization": logined_user["accessToken"]},
        )
        assert resp.status_code == 200 and resp.json()["success"]

    @allure.title("Успешное создание заказа без авторизации")
    @pytest.mark.parametrize("num", [2])
    def test_create_order_unauthorized_success(self, get_some_ingrs):
        resp = requests.post(BR.ORDERS, json=get_some_ingrs)
        assert resp.status_code == 200 and resp.json()["success"]

    @allure.title("Неуспешное создание заказа без игредиентов")
    @pytest.mark.parametrize("num", [0])
    def test_create_order_without_ingrs_fail(self, get_some_ingrs):
        resp = requests.post(BR.ORDERS, json=get_some_ingrs)
        assert resp.status_code == 400 and resp.json()["message"] == e.ingrs_err

    @allure.title("Неуспешное создание заказа c неверным хешем игредиентов")
    def test_create_order_invalid_hash_fail(self):
        params = {"ingredients": [0, 1]}
        resp = requests.post(BR.ORDERS, json=params)
        assert resp.status_code == 500


@allure.feature("Метод получения заказов конкретного пользователя")
class TestGetOrdersUser:
    @allure.title("Получение заказов конкретного пользователя авторизованного")
    def test_get_orders_authtorized_success(self, logined_user):
        resp = requests.get(
            BR.ORDERS, headers={"Authorization": logined_user["accessToken"]}
        )
        assert resp.status_code == 200

    @allure.title("Получение заказов конкретного пользователя неавторизованного")
    def test_get_orders_unauthtorized_fail(self):
        resp = requests.get(BR.ORDERS)
        assert resp.status_code == 401 and resp.json()["message"] == e.authorized
