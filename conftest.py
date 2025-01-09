import pytest
from utils.user import User
from utils.order import Order
import random


@pytest.fixture(scope='function')
def created_user():
    user = User()
    created_user = user.create_user()
    access_token = created_user['accessToken']
    yield created_user
    user.delete_user(access_token)


@pytest.fixture(scope='function')
def logined_user(created_user):
    user = User()
    user.login_user(created_user)
    access_token = created_user['accessToken']
    yield created_user
    user.delete_user(access_token)


@pytest.fixture()
def get_some_ingrs(num):
    order = Order()
    data = order.get_ingredients_dict()
    random_ids = random.sample(list(data.keys()), num)
    params = {"ingredients": random_ids}
    yield params
