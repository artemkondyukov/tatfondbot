import requests
import datetime
import util.stringutil
from util.botutil import CITY_URL, EXCHANGE_RATE_URL
from util.maps import CITY_MAP

import util.botutil


def get_dict_from(url):
    return requests.get(url).json()


def get_exchange_rate_dynamics(code):
    url = EXCHANGE_RATE_URL + code
    response_json = get_dict_from(url)
    last_rate = response_json[-1]
    second_to_last_rate = response_json[-2]
    return {
        "Bank exchange rate": last_rate[1],
        "Buying rate": last_rate[2],
        "Buying rate dynamic": last_rate[2] - second_to_last_rate[2],
        "Selling rate": last_rate[3],
        "Selling rate dynamic": last_rate[3] - second_to_last_rate[3],
        "Last update:": datetime.datetime.fromtimestamp(last_rate[0]/1000),
    }


def get_offices(city):
    what = 2  # means that we're asking for offices
    stype = 2  # means that the result will be JSON (1 for XML)
    url = CITY_URL.format(what, stype, city)
    return get_dict_from(url)


def get_atms(city):
    what = 1  # means that we're asking for ATMs
    stype = 2  # means that the result will be JSON (1 for XML)
    url = CITY_URL.format(what, stype, city)
    return get_dict_from(url)


# offices = get_offices(14)
# atms = get_atms(14)
# current_pos = [55.7, 49.1]
# closest_offices = util.get_closest_offices(offices, current_pos)
# closest_atms = util.get_closest_offices(atms, current_pos)

# print("Closest offices:")
# for office in closest_offices:
#     print(office)
#
# print("Closest ATMs:")
# for atm in closest_atms:
#     print(atm)

# for s1 in CITY_MAP.keys():
#     l = []
#     for s2 in CITY_MAP.keys():
#         l.append(stringutil.levenshtein(s1, s2))
#     print(str(s1) + " " + str(l))

# print(stringutil.get_city_code_from_string("Я из новосибирска"))