import json
import pytest
from user import User
from order import Order
import random

@pytest.fixture()
def user_data():
    user = User()
    user_data = user.generate_user_data()
    yield user_data



@pytest.fixture()
def delete_user(access_token):
    user = User()
    resp = user.delete_user(access_token)
    assert resp ==200


@pytest.fixture()
def logined_user():
    user = User()
    created_user, resp = user.create_user()
    access_token = resp['accessToken']
    user.login_user(created_user)
    yield created_user, access_token
    user.delete_user(access_token)



@pytest.fixture()
def created_user():
    user = User()
    created_user, resp = user.create_user()
    access_token = resp['accessToken']
    yield created_user
    user.delete_user(access_token)

@pytest.fixture()
def get_some_ingrs(num):
    order = Order()
    data = order.get_ingredients_dict()
    random_ids = random.sample(list(data.keys()), num)
    params = {"ingredients": random_ids}
    yield params
