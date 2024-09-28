import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"
class TestCreateOrder:
    @pytest.mark.parametrize("color", [
        ["BLACK"],         # Один цвет
        ["GREY"],          # Другой цвет
        ["BLACK", "GREY"], # Оба цвета
        []                 # Без цвета
    ])
    def test_create_order_with_various_colors(self, create_order, color):
        response = create_order(color)
        assert response.status_code == 201, f"Ожидался код 201, но вернулся {response.status_code}"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит 'track'."

    # Проверка, что заказ создается без указания цвета
    def test_create_order_without_color(self, create_order):
        response = create_order()
        assert response.status_code == 201, f"Ожидался код 201, но вернулся {response.status_code}"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит 'track'."
