import os
import telebot
import speech.recognizer as rc
from pocketsphinx import Pocketsphinx, AudioFile, get_model_path

from query_handler import QueryHandler

with open("./sensitive") as f:
    BOT_TOKEN = f.readline()

MODEL_DIR = "./model/"
# MODEL_DIR = get_model_path()

bot = telebot.TeleBot(BOT_TOKEN)
# bot.polling(none_stop=True)
handler = QueryHandler()

config = {
            'sampling_rate': 8000,
            'verbose': True,
            'hmm': os.path.join(MODEL_DIR, 'zero/zero_ru.cd_cont_4000/'),
            'lm': os.path.join(MODEL_DIR, 'zero/ru.lm'),
            'dict': os.path.join(MODEL_DIR, 'zero/ru.dic')
        }
# print(os.path.join(MODEL_DIR, 'en-us'))
# print(os.path.join(MODEL_DIR, 'cmudict-en-us.dict'))
# config = {
#             'verbose': True,
#             'hmm': os.path.join(MODEL_DIR, 'en-us'),
#             'lm': os.path.join(MODEL_DIR, 'en-us.lm.bin'),
#             'dict': os.path.join(MODEL_DIR, 'cmudict-en-us.dict')
#         }
# sphinx = AudioFile(**config)
sphinx = []
print("FUCK YOU")


@bot.message_handler(content_types=["text", "location", "voice"])
def repeat_all_messages(message):
    print(123)
    print(message)

    if message.content_type == "location":
        result = handler.process_location(message.location)
        bot.send_message(message.chat.id, str(result))
    elif message.content_type == "text":
        result = handler.process_query(message.text)
        print(result)
        for v in result:
            if len(v) > 0:
                bot.send_message(message.chat.id, v)
    elif message.content_type == 'voice':
        text = rc.recognize(bot, message.voice.file_id, sphinx)
        print(text)
        # bot.send_message(message.chat.id, text)
        if text is not None:
            result = handler.process_query(text)
            print(result)
            for v in result:
                if len(v) > 0:
                    bot.send_message(message.chat.id, v)
    else:
        print(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
