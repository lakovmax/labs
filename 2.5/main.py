import requests, json, telebot, weather_data, random

token = '7402764822:AAHDLChuCliCkBsnguMLpkNfdWB63dcL5J4'
bot = telebot.TeleBot(token)

fact_url = "https://uselessfacts.jsph.pl/random.json?language=en"

def get_cat_image_url():
    response = requests.get("https://api.thecatapi.com/v1/images/search").text
    return json.loads(response)[0]['url']

def get_useless_fact():
    response = requests.get(fact_url)
    data = response.json()
    return data["text"]

def roll_dice():
    return random.randint(1, 6)

def get_random_number():
    return random.randint(1, 100)

keyword = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyword.row('Мяу', 'Погода', 'Случайный факт', 'Кубик', 'Число')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, text="Привет!\nВыберите действие:", reply_markup=keyword)

@bot.message_handler(func=lambda message: message.text == 'Мяу')
def send_cat_image(message):
    image_url = get_cat_image_url()
    bot.send_photo(message.chat.id, photo=image_url, reply_markup=keyword)

@bot.message_handler(func=lambda message: message.text == 'Погода')
def ask_city(message):
    bot.send_message(message.chat.id, "Напишите название города, чтобы узнать погоду:")
    bot.register_next_step_handler(message, send_weather_data)

def send_weather_data(message):
    data = weather_data.get_weather_data(message.text)
    bot.send_message(message.chat.id, data)

@bot.message_handler(func=lambda message: message.text == 'Случайный факт')
def send_useless_fact(message):
    fact = get_useless_fact()
    bot.send_message(message.chat.id, fact, reply_markup=keyword)

@bot.message_handler(func=lambda message: message.text == 'Кубик')
def roll_the_dice(message):
    result = roll_dice()
    bot.send_message(message.chat.id, f"Выпало: {result}", reply_markup=keyword)

@bot.message_handler(func=lambda message: message.text == 'Число')
def send_random_number(message):
    number = get_random_number()
    bot.send_message(message.chat.id, f"Случайное число от 1 до 100: {number}", reply_markup=keyword)

bot.infinity_polling()