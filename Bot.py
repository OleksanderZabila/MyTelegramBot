import telebot
import config 
bot = telebot.Telebot(config.TOKEN)
@bot.message_handler(contetn_types=['text'])
 def text_bot(message):
     bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)
