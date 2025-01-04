import json
import pytest
from user import User
@pytest.fixture()
def user_data():
    user = User()
    user_data = user.generate_user_data()
    yield user_data
    # if courier.created_courier:
    #     courier.login_courier()
    #     courier.delete_courier()


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

