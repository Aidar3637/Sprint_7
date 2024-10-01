import pytest
import requests
from tests.data.urls import BASE_URL, COURIER_ENDPOINT, COURIER_LOGIN_ENDPOINT, ORDER_ENDPOINT
from tests.data.test_data import ORDER_PAYLOAD, COURIER_PAYLOAD

# Фикстура для создания курьера
@pytest.fixture
def create_courier():
    def _create_courier(login, password, first_name=None):
        payload = COURIER_PAYLOAD.copy()
        payload['login'] = login
        payload['password'] = password
        if first_name is not None:
            payload['firstName'] = first_name
        response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", json=payload)
        return response
    return _create_courier

# Фикстура для удаления курьера
@pytest.fixture
def delete_courier():
    def _delete_courier(courier_id):
        if courier_id:
            requests.delete(f"{BASE_URL}{COURIER_ENDPOINT}/{courier_id}")
    return _delete_courier

# Фикстура для авторизации курьера
@pytest.fixture
def login_courier():
    def _login_courier(login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", json=payload)
        return response
    return _login_courier

# Фикстура для создания заказа
@pytest.fixture
def create_order():
    def _create_order(color=None):
        payload = ORDER_PAYLOAD.copy()
        if color is not None:
            payload['color'] = color
        response = requests.post(f"{BASE_URL}{ORDER_ENDPOINT}", json=payload)
        return response
    return _create_order

# Фикстура для получения списка заказов
@pytest.fixture
def get_order_list():
    def _get_order_list():
        params = {"limit": 10}  # Укажите необходимые параметры
        response = requests.get(f"{BASE_URL}{ORDER_ENDPOINT}", params=params)
        return response
    return _get_order_list
