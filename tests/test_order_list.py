import pytest
import allure
from tests.data.test_data import EXPECTED_STATUS_CODE_ORDER_LIST, EXPECTED_ORDERS_KEY

class TestOrderList:

    @allure.title("Проверка, что в теле ответа возвращается список заказов")
    def test_order_list_contains_orders(self, get_order_list):
        response = get_order_list()
        assert response.status_code == EXPECTED_STATUS_CODE_ORDER_LIST, f"Ожидался код {EXPECTED_STATUS_CODE_ORDER_LIST}, но вернулся {response.status_code}"
        response_data = response.json()
        assert EXPECTED_ORDERS_KEY in response_data, f"Ответ не содержит ключ '{EXPECTED_ORDERS_KEY}'."
        assert isinstance(response_data[EXPECTED_ORDERS_KEY], list), f"Поле '{EXPECTED_ORDERS_KEY}' должно быть списком."
        assert len(response_data[EXPECTED_ORDERS_KEY]) > 0, "Список заказов пуст."
