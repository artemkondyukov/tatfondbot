from util.maps import CITY_MAP
# import speech_recognition

def levenshtein(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_city_code(city_name):
    keys = list(CITY_MAP.keys())
    index = 0
    minimum = 9999999
    for i, key in enumerate(keys):
        dist = levenshtein(key, city_name)
        if dist < minimum:
            minimum = dist
            index = i
    is_exact = True if minimum == 0 else False
    return CITY_MAP[keys[index]], minimum, is_exact


def get_city_code_from_string(string):
    words = string.split(" ")
    best_code = -1
    minimum_score = 9999999
    for word in words:
        code, minimum, _ = get_city_code(word)
        if minimum < minimum_score:
            minimum_score = minimum
            best_code = code
    return best_code


def get_pretty_offices(ugly):
    result = "Ближайшие к вам отделения:\n"
    for i, ug in enumerate(ugly):
        result += str(i) + ". Адрес: " + \
            + ug["Address"] + ". Время работы для физических лиц: " + \
            + ug["TIMEFIZ"] + "; Время работы для юридических лиц: " + \
            + ug["TIMEUR"] + ". "
        if ug["PHONE"] != "":
            result += "Телефон: " + ug["PHONE"] + "."
        result += "\n"
    return result


def get_pretty_atms(ugly):
    result = "Ближайшие к вам банкоматы:\n"
    for i, ug in enumerate(ugly):
        result += str(i) + ". Адрес: " + \
                  + ug["Address"] + ". Тип банкомата: " + \
                  + ug["Title"] + ". "
        if ug["TIMEALL"]:
            result += "Время работы: круглосуточно. "
        elif ug["TIME"]:
            result += "Время работы: " + ug["TIME"] + ". "
        result += "\n"
    return result


def get_pretty_exchange(ugly, currency):
    result = "Валютная пара: " + currency + "/RUB. "
    result += "Курс ЦБ: " + ugly["Bank exchange rate"] + ".\n"
    result += "Продажа: " + ugly["Selling rate"] + ", динамика: {0:.2f}".format(ugly["Selling rate dynamic"]) + ".\n"
    result += "Покупка: " + ugly["Buying rate"] + ", динамика: {0:.2f}".format(ugly["Buying rate dynamic"]) + ".\n"
    result += "Дата последнего изменения: " + ugly["Last update"].strftime("21/11/06 16:30", "%d/%m/%y %H:%M") + ".\n"
    return result
