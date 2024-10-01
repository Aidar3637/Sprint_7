import pytest
import requests
import allure
from tests.helpers import generate_unique_login
from tests.data.urls import BASE_URL, COURIER_LOGIN_ENDPOINT

class TestCourierLogin:

    @allure.title("1. Курьер может авторизоваться")
    def test_courier_can_login(self, create_courier, login_courier, delete_courier):
        login = generate_unique_login()
        password = "login_password"
        first_name = "Login"

        create_response = create_courier(login, password, first_name)
        assert create_response.status_code == 201
        courier_id = create_response.json().get("id")

        login_response = login_courier(login, password)
        assert login_response.status_code == 200
        assert "id" in login_response.json()

        delete_courier(courier_id)

    @allure.title("2. Для авторизации нужно передать все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, missing_field):
        payload = {
            "login": "test_login",
            "password": "test_password"
        }
        # Передаём пустую строку вместо удаления поля
        payload[missing_field] = ""
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", json=payload)
        assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"

    @allure.title("3. Система вернёт ошибку, если неправильно указать логин или пароль")
    def test_login_incorrect_credentials(self):
        payload = {
            "login": "nonexistent_login",
            "password": "wrong_password"
        }
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", json=payload)
        assert response.status_code == 404, f"Ожидался код 404, но получен {response.status_code}"
        response_data = response.json()
        assert response_data.get("message") == "Учетная запись не найдена", "Сообщение об ошибке не соответствует ожиданиям"

    @allure.title("4. Если какого-то поля нет, запрос возвращает ошибку")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_error(self, missing_field):
        payload = {
            "login": "test_login",
            "password": "test_password"
        }
        # Передаём пустую строку вместо удаления поля
        payload[missing_field] = ""
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", json=payload)
        assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"
        response_data = response.json()
        assert response_data.get("message") == "Недостаточно данных для входа", "Сообщение об ошибке не соответствует ожиданиям"

    @allure.title("5. Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_login_non_existent_user(self):
        payload = {
            "login": "nonexistent_login",
            "password": "wrong_password"
        }
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", json=payload)
        assert response.status_code == 404, f"Ожидался код 404, но получен {response.status_code}"
        response_data = response.json()
        assert response_data.get("message") == "Учетная запись не найдена", "Сообщение об ошибке не соответствует ожиданиям"

    @allure.title("6. Успешный запрос возвращает id")
    def test_login_returns_id(self, create_courier, login_courier, delete_courier):
        login = generate_unique_login()
        password = "login_password"
        first_name = "Login"

        create_response = create_courier(login, password, first_name)
        assert create_response.status_code == 201
        courier_id = create_response.json().get("id")

        login_response = login_courier(login, password)
        assert login_response.status_code == 200
        assert "id" in login_response.json()

        delete_courier(courier_id)
