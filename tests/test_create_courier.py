import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

# Вспомогательная функция для создания тела запроса
def create_courier_payload(login, password="test_password", first_name="Test"):
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }
class TestCourierCreation:

    # 1. Курьера можно создать.
    def test_create_courier(self, create_courier, delete_courier, unique_login):
        response = create_courier(unique_login, "unique_password", "Unique")
        assert response.status_code == 201
        assert response.json()["ok"] == True
        courier_id = response.json().get("id")
        delete_courier(courier_id)

    # 2. Нельзя создать двух одинаковых курьеров.
    def test_create_duplicate_courier(self, create_courier, delete_courier, unique_login):
        response = create_courier(unique_login, "duplicate_password", "Duplicate")
        assert response.status_code == 201
        courier_id = response.json().get("id")
        response_duplicate = create_courier(unique_login, "duplicate_password", "Duplicate")
        assert response_duplicate.status_code == 409
        delete_courier(courier_id)

    # 3. Чтобы создать курьера, нужно передать в ручку все обязательные поля.
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_create_courier_missing_field(self, field, unique_login):
        payload = create_courier_payload(unique_login)
        payload.pop(field)
        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 400  # Поля login и password обязательны

    # Новый тест для проверки необязательных полей
    def test_create_courier_optional_field(self, unique_login):
        payload = create_courier_payload(unique_login, first_name=None)
        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 201  # Поле firstName необязательное

    # 4. Запрос возвращает правильный код ответа.
    def test_create_courier_status_code(self, create_courier, delete_courier, unique_login):
        response = create_courier(unique_login, "status_password", "Status")
        assert response.status_code == 201
        courier_id = response.json().get("id")
        delete_courier(courier_id)

    # 5. Успешный запрос возвращает {"ok":true}.
    def test_create_courier_response(self, create_courier, delete_courier, unique_login):
        response = create_courier(unique_login, "response_password", "Response")
        assert response.json()["ok"] == True
        courier_id = response.json().get("id")
        delete_courier(courier_id)

    # 7. Если создать пользователя с логином, который уже есть, возвращается ошибка.
    def test_create_courier_with_existing_login(self, create_courier, delete_courier, unique_login):
        response = create_courier(unique_login, "existing_password", "Existing")
        assert response.status_code == 201
        courier_id = response.json().get("id")
        response_duplicate = create_courier(unique_login, "existing_password", "Existing")
        assert response_duplicate.status_code == 409
        delete_courier(courier_id)
