import telebot

bot = telebot.TeleBot("6637738833:AAH9lmzTbk6SWrQC5SM4a3eECy56fU6KZfo")

@bot.message_handler(commands=['start'])
def start(message):
     mess = f'hi,<b> {message.from_user.first_name} {message.from_user.last_name}</b>'
     bot.send_message(message.chat.id, mess, parse_mode='html')
     photo = open('D:\PythotProjects\MyTelegramBot\PhotoBot\photo1.png', 'rb')
     bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_com = f'hi my name <b>Szabilatestbot<b> i help u user you to me' \
               f'<b>/start</b> - its command welcome to you and send photo' \
               f'<b>hello</b>  - send welcome' \
               f'<b>id</b>     - send you id telegram<' \
               f'<b>dear other command dont understand of bot</b>'
    bot.send_message(message.chat.id, help_com) #parse_mode='html' (dont work)

@bot.message_handler()
def get_user(message):
     if message.text == "hello":
        bot.send_message(message.chat.id, "ОООО дарова")
     elif message.text == "id":
        bot.send_message(message.chat.id, f"U Id {message.chat.id}")
     else:
        bot.send_message(message.chat.id, f"im dont ander stend")



bot.polling(none_stop=True)
