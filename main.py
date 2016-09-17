import telebot

with open("./sensitive") as f:
    BOT_TOKEN = f.readline()

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
