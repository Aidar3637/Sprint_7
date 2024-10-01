import random
import string

def generate_unique_login():
    return "user_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def create_courier_payload(login, password="test_password", first_name="Test"):
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

def check_login_response(response, expected_status_code):
    assert response.status_code == expected_status_code, f"Ожидался код {expected_status_code}, но получен {response.status_code}"
    response_data = response.json()
    if expected_status_code == 200:
        assert "id" in response_data, "В ответе отсутствует поле 'id'"
    else:
        assert "message" in response_data, "В ответе отсутствует поле 'message'"
