import requests
from utils.routes import BurgerRoutes as BR


class Order:
    def get_ingredients_dict(self):
        ingrs = requests.get(BR.INGRS).json()
        if ingrs.get("success"):
            data_list = ingrs.get("data", [])
            result_dict = {item["_id"]: item["name"] for item in data_list}
        else:
            result_dict = {}
        return result_dict
