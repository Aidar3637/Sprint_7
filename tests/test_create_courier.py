import pytest
import requests
import allure
from tests.helpers import generate_unique_login
from tests.data.urls import BASE_URL, COURIER_ENDPOINT

class TestCourierCreation:

    @allure.title("1. Курьера можно создать")
    def test_create_courier(self, create_courier, delete_courier, login_courier):
        login = generate_unique_login()
        password = "unique_password"
        first_name = "Unique"

        # Создаем курьера
        response = create_courier(login, password, first_name)

        # Проверяем успешность создания
        response_data = response.json()
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"
        assert response_data.get("ok") == True, "Курьер не был создан"

        # Логинимся, чтобы получить courier_id
        login_response = login_courier(login, password)
        courier_id = login_response.json().get("id")
        assert courier_id is not None, "Не удалось получить ID курьера при логине"

        # Очистка после теста
        delete_courier(courier_id)

    @allure.title("2. Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, create_courier, delete_courier, login_courier):
        login = generate_unique_login()
        password = "duplicate_password"
        first_name = "Duplicate"

        # Создаем первого курьера
        create_courier(login, password, first_name)

        # Пытаемся создать курьера с тем же логином
        response_duplicate = create_courier(login, password, first_name)

        # Ключевая проверка: создание дубликата должно вернуть статус 409
        assert response_duplicate.status_code == 409, f"Ожидался статус 409, но получен {response_duplicate.status_code}"
        response_data = response_duplicate.json()
        expected_message = "Этот логин уже используется. Попробуйте другой."
        assert response_data.get("message") == expected_message, "Сообщение об ошибке не соответствует ожиданиям"

        # Очистка после теста
        login_response = login_courier(login, password)
        courier_id = login_response.json().get("id")
        delete_courier(courier_id)

    @allure.title("3. Чтобы создать курьера, нужно передать в ручку все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        login = generate_unique_login()
        password = "test_password"
        first_name = "Test"

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        payload.pop(missing_field)

        response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", json=payload)

        # Ключевая проверка: отсутствие обязательного поля должно вернуть статус 400
        assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
        response_data = response.json()
        expected_message = "Недостаточно данных для создания учетной записи"
        assert response_data.get("message") == expected_message, "Сообщение об ошибке не соответствует ожиданиям"

    @allure.title("4. Поле firstName необязательное")
    def test_create_courier_optional_field(self, create_courier, delete_courier, login_courier):
        login = generate_unique_login()
        password = "test_password"

        # Создаем курьера без firstName
        response = create_courier(login, password)
        response_data = response.json()

        # Ключевая проверка: курьер должен быть успешно создан без firstName
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"
        assert response_data.get("ok") == True, "Курьер не был создан без firstName"

        # Логинимся, чтобы получить courier_id
        login_response = login_courier(login, password)
        courier_id = login_response.json().get("id")
        assert courier_id is not None, "Не удалось получить ID курьера при логине"

        # Очистка после теста
        delete_courier(courier_id)

    @allure.title("5. Запрос возвращает правильный код ответа")
    def test_create_courier_status_code(self, create_courier, delete_courier, login_courier):
        login = generate_unique_login()
        password = "status_password"
        first_name = "Status"

        # Создаем курьера
        response = create_courier(login, password, first_name)

        # Ключевая проверка: проверяем статус код
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"

        # Логинимся, чтобы получить courier_id
        login_response = login_courier(login, password)
        courier_id = login_response.json().get("id")
        delete_courier(courier_id)

    @allure.title("6. Успешный запрос возвращает {{'ok': true}}")
    def test_create_courier_response(self, create_courier, delete_courier, login_courier):
        login = generate_unique_login()
        password = "response_password"
        first_name = "Response"

        # Создаем курьера
        response = create_courier(login, password, first_name)
        response_data = response.json()

        # Ключевая проверка: проверяем, что в ответе есть 'ok': true
        assert response_data.get("ok") == True, "Ответ не содержит 'ok': true"

        # Логинимся, чтобы получить courier_id
        login_response = login_courier(login, password)
        courier_id = login_response.json().get("id")
        delete_courier(courier_id)

    @allure.title("7. Если создать пользователя с логином, который уже есть, возвращается ошибка")
    def test_create_courier_with_existing_login(self, create_courier, delete_courier, login_courier):
        login = generate_unique_login()
        password = "existing_password"
        first_name = "Existing"

        # Создаем первого курьера
        create_courier(login, password, first_name)

        # Пытаемся создать курьера с тем же логином
        response_duplicate = create_courier(login, password, first_name)

        # Ключевая проверка: должно вернуться 409 Conflict
        assert response_duplicate.status_code == 409, f"Ожидался статус 409, но получен {response_duplicate.status_code}"
        response_data = response_duplicate.json()
        expected_message = "Этот логин уже используется. Попробуйте другой."
        assert response_data.get("message") == expected_message, "Сообщение об ошибке не соответствует ожиданиям"

        # Очистка после теста
        login_response = login_courier(login, password)
        courier_id = login_response.json().get("id")
        delete_courier(courier_id)
