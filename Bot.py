import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import datetime
import time
import schedule
import threading
import sys

bot = telebot.TeleBot("6637738833:AAH9lmzTbk6SWrQC5SM4a3eECy56fU6KZfo")

def stop_bot(message):
    bot.send_message(message.chat.id, "Бот зупинено за командою /stop.")
    sys.exit(0)

config_file = "time.txt"
reminder_mode = False  # Змінна для відстеження режиму встановлення нагадувань

# Завантаження нагадувань з файлу конфігурації
def load_reminders():
    try:
        with open(config_file, "r") as f:
            reminders = {}
            for line in f:
                time_str, reminder_text, days = line.strip().split(":", 2)
                reminders[time_str] = (reminder_text, days.split(","))
            return reminders
    except FileNotFoundError:
        return {}

# Збереження нагадувань у файл конфігурації
def save_reminders(reminders):
    with open(config_file, "w") as f:
        for time_str, (reminder_text, days) in reminders.items():
            f.write(f"{time_str}:{reminder_text}:{','.join(days)}\n")

# Функція для відправки нагадувань
def send_reminders():
    current_day = datetime.datetime.now().strftime("%a").lower()
    reminders = load_reminders()
    for time_str, (reminder_text, days) in reminders.items():
        if current_day in days and datetime.datetime.now().strftime("%H:%M") == time_str:
            bot.send_message(CHAT_ID, f"Нагадування: {reminder_text}")

# Додаємо щоденне виконання функції send_reminders через бібліотеку schedule
schedule.every().day.at("00:01").do(send_reminders)

# Функція для запуску send_reminders() в фоновому режимі
def run_send_reminders():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Команда для встановлення нагадування
@bot.message_handler(func=lambda message: message.text == 'Зробити нагадування⏰')
def set_reminder(message):
    global reminder_mode
    reminder_mode = True  # Увімкнення режиму встановлення нагадувань
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    days_of_week = ["пн", "вт", "ср", "чт", "пт", "сб", "нд"]
    keyboard.add(*[telebot.types.KeyboardButton(day) for day in days_of_week])
    bot.send_message(message.chat.id, "Введіть час і текст нагадування у форматі 'ЧЧ:ММ:Текст'\n 13:30:Поснідать:", reply_markup=keyboard)

# Обробник для збереження введеного нагадування
@bot.message_handler(func=lambda message: reminder_mode)
def handle_reminder_input(message):
    global reminder_mode
    try:
        time_str, reminder_text = message.text.strip().split(":", 1)
        datetime.datetime.strptime(time_str, "%H:%M")
        reminders = load_reminders()
        reminders[time_str] = (reminder_text, [])
        bot.register_next_step_handler(message, choose_days, time_str, reminders)
        bot.send_message(message.chat.id, "Виберіть дні тижня для нагадування:", reply_markup=telebot.types.ReplyKeyboardRemove())
    except ValueError:
        bot.send_message(message.chat.id, "Невірний формат. Введіть час і текст нагадування у форматі 'ЧЧ:ММ:Текст'.")
        reminder_mode = False  # Вимкнення режиму встановлення нагадувань

# Функція для вибору днів тижня
def choose_days(message, time_str, reminders):
    global reminder_mode
    if message.text.lower() == "готово":
        save_reminders(reminders)
        bot.send_message(message.chat.id, f"Нагадування '{reminders[time_str][0]}' встановлено на {time_str} у дні: {', '.join(reminders[time_str][1])}.")
    else:
        days_of_week = ["пн", "вт", "ср", "чт", "пт", "сб", "нд"]
        if message.text.lower() in days_of_week:
            reminders[time_str][1].append(message.text.lower())
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(day) for day in days_of_week])
        keyboard.add("Готово")
        bot.send_message(message.chat.id, f"Вибрані дні тижня: {', '.join(reminders[time_str][1])}. Виберіть ще дні або натисніть 'Готово':", reply_markup=keyboard)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Привіт🖐')
    button2 = telebot.types.KeyboardButton('Допомога')
    button3 = telebot.types.KeyboardButton('Зробити нагадування⏰')
    keyboard.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Виберіть дію:", reply_markup=keyboard)

# Команда /hi
@bot.message_handler(commands=['hi'])
def hi(message):
    mess = f'Привіт, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    photo = open('D:\PythotProjects\MyTelegramBot\PhotoBot\photo1.png', 'rb')
    bot.send_photo(message.chat.id, photo)

# Обробник команди /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_com = f'Привіт! Я бот <b>Szabilatestbot</b> і я допомагаю вам. Ось деякі команди:\n' \
               f'<b>/hi</b> - привітання та відправка фото\n' \
               f'<b>/help</b>  - відправка привітання\n' \
               f'<b>/id</b>     - відправка вашого ID в Telegram\n' \
               f'<b>/setreminder</b> - установка нагадувань\n' \
               f'Для встановлення нагадувань, використовуйте команду /setreminder\n'
    bot.send_message(message.chat.id, help_com, parse_mode='html')

# Обробник інших повідомлень
@bot.message_handler(func=lambda message: True)
def get_user(message):
    if message.text == "Привіт🖐":
        hi(message)
    elif message.text == "Допомога":
        help_command(message)
    else:
        bot.send_message(message.chat.id, "Я не розумію цю команду. Спробуйте іншу.")

# Запускаємо бота в окремому потоці
def run_bot():
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        sys.exit(0)

# Запускаємо бота
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

# Запускаємо функцію run_send_reminders у окремому потоці
reminder_thread = threading.Thread(target=run_send_reminders)
reminder_thread.start()
