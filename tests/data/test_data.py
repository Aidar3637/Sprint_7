# Данные для тестов создания заказа
CREATE_ORDER_COLORS = [
    ["BLACK"],         # Один цвет
    ["GREY"],          # Другой цвет
    ["BLACK", "GREY"], # Оба цвета
    []                 # Без цвета
]

EXPECTED_STATUS_CODE = 201
EXPECTED_TRACK_FIELD = "track"

ORDER_PAYLOAD = {
    "firstName": "Test",
    "lastName": "User",
    "address": "Test Address",
    "metroStation": 4,
    "phone": "+7 800 555 35 35",
    "rentTime": 5,
    "deliveryDate": "2023-10-10",
    "comment": "Test comment",
}

# Данные для курьера
COURIER_PAYLOAD = {
    "login": "",
    "password": "",
    "firstName": ""
}
# Ожидаемые значения для тестов списка заказов
EXPECTED_STATUS_CODE_ORDER_LIST = 200
EXPECTED_ORDERS_KEY = "orders"
