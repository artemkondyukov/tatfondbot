import signal
from logging import Handler

import requests
from pip.utils import logging
import sys
from tornado import web, ioloop

with open("./sensitive") as f:
    BOT_TOKEN = f.readline()


def signal_term_handler(signal, frame):
    print('got SIGTERM/SIGINT')
    sys.exit(0)


URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
MyURL = "localhost/hook"

api = requests.Session()
application = web.Application([
    (r"/", Handler),
])

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        set_hook = api.get(URL + "setWebhook?url=%s" % MyURL)
        if set_hook.status_code != 200:
            logging.error("Can't set hook: %s. Quit." % set_hook.text)
            exit(1)
        application.listen(8888)
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        signal_term_handler(signal.SIGTERM, None)
