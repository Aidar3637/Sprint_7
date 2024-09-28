import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
@pytest.fixture
def unique_login():
    return "user_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@pytest.fixture
def create_courier():
    def _create_courier(login, password, first_name):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        return response
    return _create_courier

@pytest.fixture
def delete_courier():
    def _delete_courier(courier_id):
        if courier_id:
            requests.delete(f"{BASE_URL}/courier/{courier_id}")
    return _delete_courier

@pytest.fixture
def login_courier():
    def _login_courier(login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        return response
    return _login_courier

@pytest.fixture
def create_order():
    def _create_order(color=None):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": 4,
            "phone": "+7 800 555 35 35",
            "rentTime": 5,
            "deliveryDate": "2023-10-10",
            "comment": "Test comment",
            "color": color if color else []
        }
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        return response
    return _create_order

@pytest.fixture
def get_order_list():
    def _get_order_list():
        response = requests.get(f"{BASE_URL}/orders")
        return response
    return _get_order_list
