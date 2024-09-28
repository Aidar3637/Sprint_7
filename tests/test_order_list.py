import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"
class TestOrderList:

    # Проверка, что в теле ответа возвращается список заказов.
    def test_order_list_contains_orders(self, get_order_list):
        response = get_order_list()
        assert response.status_code == 200, f"Ожидался код 200, но вернулся {response.status_code}"
        response_data = response.json()
        assert "orders" in response_data, "Ответ не содержит ключ 'orders'."
        assert isinstance(response_data["orders"], list), "Поле 'orders' должно быть списком."
        assert len(response_data["orders"]) > 0, "Список заказов пуст."
