from faker import Faker
import allure
import requests
from routes import BurgerRoutes as r

class Order:
    def get_ingredients_dict(self):
        ingrs = requests.get(r.INGRS).json()
        if ingrs.get("success"):
            data_list = ingrs.get("data", [])
            result_dict = {item["_id"]: item["name"] for item in data_list}
        else:
            result_dict = {}
        return result_dict
