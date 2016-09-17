import math

EXCHANGE_RATE_URL = "https://app.tfb.ru/services/courses/data?code="
CITY_URL = "https://tfb.ru/points.php?what={}&type={}&city={}"

CITY_MAP = {
    "Воронеж": 270,
    "Екатеринбург": 628,
    "Ижевск": 194,
    "Йошкар-Ола": 284,
    "Москва": 16,
    "Новосибирск": 79,
    "Пермь": 80,
    "Ярославль": 361,
    "Белебей": 630,
    "Белорецк": 771,
    "Кумертау": 625,
    "Уфа": 254,
    "Агрыз": 72,
    "Азнакаево": 61,
    "Актаныш": 73,
    "Алексеевское": 86,
    "Альметьевск": 60,
    "Апастово": 50,
    "Арск": 51,
    "Бавлы": 63,
    "Балтаси": 52,
    "Буинск": 54,
    "Джалиль": 65,
    "Елабуга": 69,
    "Заинск": 74,
    "Зеленодольск": 70,
    "Казань": 14,
    "Кукмор": 58,
    "Лениногорск": 66,
    "Мензелинск": 75,
    "Муслюмово": 67,
    "Новошешминск": 87,
    "Нурлат": 88,
    "Чебоксары": 83,
    "Арзамас": 629,
    "Дзержинск": 626,
    "Тольятти": 603,
    "Саратов": 196,
}


def get_closest_offices(office_list, position):
    """
    Could use for ATMs also
    :param office_list: List of offices (or ATMs)
    :param position: Current position of the client
    :return:
    """
    list_to_order = []
    for office in office_list:
        coord = [float(c) for c in office["Coordinates"]]
        distance = math.sqrt(math.pow(position[0] - coord[0], 2) + math.pow(position[1] - coord[1], 2))
        list_to_order.append((office["Id"], distance))

    ids = [k[0] for k in sorted(list_to_order, key=lambda x: x[1])]
    return [get_office_by_id(office_list, k) for k in ids if k is not None][:3]


def get_office_by_id(office_list, office_id):
    for office in office_list:
        if office["Id"] == office_id:
            return office
    return None
