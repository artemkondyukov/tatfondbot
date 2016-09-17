from util.stringutil import levenshtein, get_pretty_exchange, get_pretty_offices, get_pretty_atms, get_text_from_texts
from util.requestutil import *
from util.maps import *
from util.botutil import *


class QueryHandler:
    def __init__(self):
        self.term_map = {
            "банк": "office",
            "банкомат": "atm",
            "курс": ("currency", None),
            "доллар": ("currency", "USD")
        }
        self.function_map = {
            "currency": self.currency_info,
            "office": self.find_offices,
            "atm": self.find_atms
        }
        self.info_required_message = {
            "location": "Пришлите, пожалуйста, Ваше местоположение"
        }
        self.LEVENSHTEIN_THRESHOLD = 3
        self.response = {"pending": set()}
        self.required_info = dict()
        self.request_info = None

    def get_map_key_fuzzy(self, token, map):
        result = []
        for key in map:
            if levenshtein(token, key) < self.LEVENSHTEIN_THRESHOLD:
                result.append((key, levenshtein(token, key)))

        min_distance = 10e9
        closest = None
        for r in result:
            if r[1] < min_distance:
                closest = r
                min_distance = r[1]

        return closest[0] if closest is not None else None

    def is_token_similar(self, token, term):
        if levenshtein(token, term) <= self.LEVENSHTEIN_THRESHOLD:
            return True
        return False

    def process_query(self, query):
        print(query)
        query_tokens = query.split(" ")
        self.request_info = dict()
        for token in query_tokens:
            if token in BANK_SERVICES:
                return get_text_from_texts(BANK_SERVICES[token]), ""
            if token in CURRENCY_INDEX:
                self.request_info["currency"] = CURRENCY_INDEX[token]
            else:
                term_fuzzy = self.get_map_key_fuzzy(token, CURRENCY_INDEX)
                if term_fuzzy is not None:
                    self.request_info["currency"] = CURRENCY_INDEX[term_fuzzy]

            if token in ACTION_INDEX:
                if ACTION_INDEX[token] not in self.request_info:
                    self.request_info[ACTION_INDEX[token]] = None
            else:
                term_fuzzy = self.get_map_key_fuzzy(token, ACTION_INDEX)
                if term_fuzzy is not None:
                    if ACTION_INDEX[term_fuzzy] not in self.request_info:
                        self.request_info[ACTION_INDEX[term_fuzzy]] = None

        response = self.provide_request_info()
        pending_info_messages = [self.info_required_message[key[0]] for key in self.response["pending"]]
        print(pending_info_messages)
        return response, "\n".join(pending_info_messages)

    def provide_request_info(self):
        result = ""
        for key in self.request_info:
            result += self.function_map[key](self.request_info[key])
        return result

    def find_offices(self, term):
        # Ask for location and find nearest offices
        if "location" not in self.response:
            self.response["pending"].add(("location", self.find_offices))
            return ""
        return str(get_closest_offices(get_offices(14),
                                       [self.response["location"].latitude,
                                       self.response["location"].longitude]))

    def find_atms(self, term):
        # Ask for location and find nearest offices

        if "location" not in self.response:
            self.response["pending"].add(("location", self.find_atms))
            return ""
        return str(get_closest_offices(get_atms(14),
                                       [self.response["location"].latitude,
                                       self.response["location"].longitude]))

    def currency_info(self, term):
        # Ask for the currency of interest (or get from query) and return the value
        if self.request_info["currency"] is None:
            return str(get_pretty_exchange(get_exchange_rate_dynamics("USD"), "USD"))
        else:
            return str(get_pretty_exchange(get_exchange_rate_dynamics(term), term))

    def process_pending(self):
        result = ""
        for p in self.response["pending"]:
            result += p[1](None)
        if result != "":
            if p[1] == self.find_offices:
                result = get_pretty_offices(result)
            elif p[1] == self.find_atms:
                result = get_pretty_atms(result)
        self.response["pending"] = set()
        return result

    def process_location(self, location):
        self.response["location"] = location
        result = self.process_pending()
        return result
