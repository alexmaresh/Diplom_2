import pytest
import requests
import allure

from routes import BurgerRoutes as r
from error_messages import ErrorMessages as e


@allure.feature("Метод создания заказа")
class TestCreateOrder:
    @allure.title("Успешное создание заказа c авторизацией и ингредиентами")
    @pytest.mark.parametrize('num', [2])
    def test_create_order_authorized_success(self, get_some_ingrs, logined_user):
        user_data, token = logined_user
        resp = requests.post(r.ORDERS, json=get_some_ingrs, headers={'Authorization': token})
        assert resp.status_code == 200 and resp.json()['success'], resp.json()

    @allure.title("Успешное создание заказа без авторизации")
    @pytest.mark.parametrize('num', [2])
    def test_create_order_unauthorized_success(self, get_some_ingrs):
        resp = requests.post(r.ORDERS, json=get_some_ingrs)
        assert resp.status_code == 200 and resp.json()['success'], resp.json()

    @allure.title("Неуспешное создание заказа без игредиентов")
    @pytest.mark.parametrize('num', [0])
    def test_create_order_without_ingrs_fail(self, get_some_ingrs):
        resp = requests.post(r.ORDERS, json=get_some_ingrs)
        assert resp.status_code == 400 and resp.json()['message']== e.ingrs_err, resp.json()

    @allure.title("Неуспешное создание заказа c неверным хешем игредиентов")
    def test_create_order_invalid_hash_fail(self):
        params = {"ingredients": [0,1]}
        resp = requests.post(r.ORDERS, json=params)
        assert resp.status_code == 500

@allure.feature("Метод получения заказов конкретного пользователя")
class TestGetOrdersUser:
    @allure.title("Получение заказов конкретного пользователя авторизованного")
    def test_get_orders_authtorized_success(self, logined_user):
        user_data, token = logined_user
        resp = requests.get(r.ORDERS, headers={'Authorization':token})
        assert resp.status_code == 200, resp.json()

    @allure.title("Получение заказов конкретного пользователя неавторизованного")
    def test_get_orders_unauthtorized_fail(self):
        resp = requests.get(r.ORDERS)
        assert resp.status_code == 401, resp.json()['message'] == e.authorized


