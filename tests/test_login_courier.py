import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

# Вспомогательная функция для создания тела логина
def login_payload(login, password):
    return {
        "login": login,
        "password": password
    }

# Вспомогательная функция для проверки ответа логина
def check_login_response(response, expected_status_code, expected_message=None):
    assert response.status_code == expected_status_code, f"Ожидался код {expected_status_code}, но пришел {response.status_code}"
    if expected_message:
        assert response.json().get("message") == expected_message, f"Ожидалось сообщение: {expected_message}"
class TestCourierLogin:

    # 1. Курьер может авторизоваться.
    def test_courier_can_login(self, create_courier, login_courier, delete_courier, unique_login):
        login = unique_login
        password = "login_password"
        first_name = "Login"

        create_response = create_courier(login, password, first_name)
        assert create_response.status_code == 201
        courier_id = create_response.json().get("id")

        login_response = login_courier(login, password)
        check_login_response(login_response, 200)
        assert "id" in login_response.json()

        delete_courier(courier_id)

    # 2. Для авторизации нужно передать все обязательные поля.
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, missing_field):
        payload = login_payload("test_login", "test_password")
        payload[missing_field] = ""  # Передаем пустое значение вместо удаления ключа
        response = requests.post(f"{BASE_URL}/login", json=payload)
        check_login_response(response, 400)

    # 3. Система вернёт ошибку, если неправильно указать логин или пароль.
    def test_login_incorrect_credentials(self, login_courier):
        # Используем заведомо неправильные данные
        response = login_courier("non_existing_user_123", "non_existing_password_123")
        if response.status_code == 200:
            # Проверяем, содержит ли ответ корректный ID
            assert "id" not in response.json(), f"Сервер вернул id {response.json().get('id')} для неверных данных."
            pytest.fail("Ожидался код ошибки, но сервер вернул успешный ответ (200).")
        check_login_response(response, 404)

    # 4. Если какого-то поля нет, запрос возвращает ошибку.
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_error(self, missing_field):
        payload = login_payload("test_login", "test_password")
        payload[missing_field] = ""  # Передаем пустое значение вместо удаления ключа
        response = requests.post(f"{BASE_URL}/login", json=payload)
        check_login_response(response, 400)

    # 5. Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку.
    def test_login_non_existent_user(self, login_courier):
        response = login_courier("non_existent_login", "non_existent_password")
        check_login_response(response, 404)

    # 6. Успешный запрос возвращает id.
    def test_login_returns_id(self, create_courier, login_courier, delete_courier, unique_login):
        login = unique_login
        password = "login_password"
        first_name = "Login"

        create_response = create_courier(login, password, first_name)
        assert create_response.status_code == 201
        courier_id = create_response.json().get("id")

        login_response = login_courier(login, password)
        check_login_response(login_response, 200)
        assert "id" in login_response.json()

        delete_courier(courier_id)
