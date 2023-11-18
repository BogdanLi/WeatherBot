import telebot as tb
from telebot import types
import requests
import json

bot = tb.TeleBot('6983479364:AAHZswdhN2Xy2g9X6Ku6UuSJygzlEwDeBfw')
api = '005f050fc8c54e128f791445231711'


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, 'Hi, write your city')


@bot.message_handler(content_types=['text'])
def get_weather(msg):
    city = msg.text.strip().lower()
    res = requests.get(f'http://api.weatherapi.com/v1/current.json?key=005f050fc8c54e128f791445231711&q={city.capitalize()}&aqi=no')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["current"]["temp_c"]
        bot.reply_to(msg, f'Now weather: {temp}')

        image = 'sunny.png' if temp > 5.0 else 'cloudy.png'
        file = open(image, 'rb')
        bot.send_photo(msg.chat.id, file)
    else:
        bot.reply_to(msg, f"{city} doesn't exist")

bot.polling(none_stop=True)