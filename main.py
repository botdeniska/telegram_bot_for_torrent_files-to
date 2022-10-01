import requests
import telebot  # $ pip install git+https://github.com/eternnoir/pyTelegramBotAPI.git
from telebot import types

# Вставляем ТОКЕН нашего бота в формате 53446321:AAHJCP6v3XA7KWJDHs8Vy9NOpqsBu1qYI
token = "5344631121:AAHJCP6v3XA7KWJDHs8Vy9NOpqsBu1qzbYI"
bot = telebot.TeleBot(token, parse_mode=None)


def get_access_status(user_id):
    if user_id == '33875441' or user_id == '365469' or user_id == '428849549':
        return True
    return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, str(message.chat.id))
    if get_access_status(str(message.chat.id)):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Фильмы")
        btn2 = types.KeyboardButton("Сериалы")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text='Выбери категорию', reply_markup=markup)

        @bot.message_handler(commands=['help'])
        def send_help(message):
            bot.reply_to(message, "Выполни команду /start что бы выбрать категорию, далее отправь мне файл")

        @bot.message_handler()
        def choose_button(message):
            with open("category.txt", "w") as f:
                f.write(str(message.text))
                f.close()
            bot.reply_to(message, 'Запомнил категорию, гони файл')

        @bot.message_handler(content_types=['document'])
        def handle_docs_asd(message):
            # bot.reply_to(message, message.document.file_id)
            url = f"https://api.telegram.org/bot{token}/getFile"
            payload = {"file_id": message.document.file_id}
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            response = requests.post(url, json=payload, headers=headers)
            with open("category.txt", "r") as f:
                folder_name = f.readline()
                f.close()

            # Прописываем путь до папки - меняем /Users/denisbabchuk/Documents/файлы
            with open(
                    f"/Users/denisbabchuk/Documents/файлы/{folder_name}/{message.document.file_name}.{message.document.file_name.split('.')[-1]}",
                    "wb") as f:
                f.write(response.content)
                f.close()
    else:
        bot.reply_to(message, "Хуй тебе")


bot.infinity_polling()
