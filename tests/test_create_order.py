import pytest
import allure
from tests.data.test_data import CREATE_ORDER_COLORS, EXPECTED_STATUS_CODE, EXPECTED_TRACK_FIELD

class TestCreateOrder:

    @allure.title("Тестирование создания заказа с различными цветами")
    @pytest.mark.parametrize("color", CREATE_ORDER_COLORS)
    def test_create_order_with_various_colors(self, create_order, color):
        response = create_order(color)
        assert response.status_code == EXPECTED_STATUS_CODE, f"Ожидался код {EXPECTED_STATUS_CODE}, но вернулся {response.status_code}"
        response_data = response.json()
        assert EXPECTED_TRACK_FIELD in response_data, f"Ответ не содержит '{EXPECTED_TRACK_FIELD}'."

    @allure.title("Проверка, что заказ создается без указания цвета")
    def test_create_order_without_color(self, create_order):
        response = create_order()
        assert response.status_code == EXPECTED_STATUS_CODE, f"Ожидался код {EXPECTED_STATUS_CODE}, но вернулся {response.status_code}"
        response_data = response.json()
        assert EXPECTED_TRACK_FIELD in response_data, f"Ответ не содержит '{EXPECTED_TRACK_FIELD}'."
