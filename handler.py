import logging
from tornado import web, escape

CMD = {"help": "1"}


class Handler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        try:
            logging.debug("Got request: %s" % self.request.body)
            update = escape.json_decode(self.request.body)
            message = update['message']
            text = message.get('text')
            if text:
                logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

                if text[0] == '/':
                    command, *arguments = text.split(" ", 1)
                    response = CMD.get(command, not_found)(arguments, message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    send_reply(response)
        except Exception as e:
            logging.warning(str(e))


def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
    for command in CMD:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response


def not_found(response):
    return "None"


def send_reply(response):
    if 'text' in response:
        api.post(URL + "sendMessage", data=response)
