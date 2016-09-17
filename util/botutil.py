import math

EXCHANGE_RATE_URL = "https://app.tfb.ru/services/courses/data?code="
CITY_URL = "https://tfb.ru/points.php?what={}&type={}&city={}"


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
