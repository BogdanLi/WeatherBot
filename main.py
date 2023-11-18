import telebot as tb
from telebot import types
import requests
import json

bot = tb.TeleBot('6983479364:AAHZswdhN2Xy2g9X6Ku6UuSJygzlEwDeBfw')
api = '005f050fc8c54e128f791445231711'

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, 'Hi, write your city')


@bot.message_handler(commands=['check_api'])
def check_api(msg):
    res = requests.get('http://api.weatherapi.com/v1/current.json?key=005f050fc8c54e128f791445231711&q=Moscow&aqi=no')

    if res.status_code == 200:
        data = json.loads(res.text)

        bot.send_message(msg.chat.id, data[::])
    else:
        bot.send_message(msg.chat.id, 'Error')


@bot.message_handler(content_types=['text'])
def get_weather(msg):
    city = msg.text.strip().lower()
    res = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api}&q={city.capitalize()}&aqi=no')
    if res.status_code == 200:
        data = json.loads(res.text)
        location = data["location"]["name"]
        temp = data["current"]["temp_c"]
        last_updated = data["current"]["last_updated"]
        status = data["current"]["condition"]["text"]
        feels_like = data["current"]["feelslike_c"]


        bot.reply_to(msg, f"Location: {location}\nTemperature: {temp}\nStatus: {status}\nFeels like: {feels_like}\nLast updated: {last_updated}")

        # image = 'sunny.png' if temp > 5.0 else 'cloudy.png'
        # file = open(image, 'rb')
        # bot.send_photo(msg.chat.id, file)
    else:
        bot.reply_to(msg, f"{city} doesn't exist")


bot.polling(none_stop=True)