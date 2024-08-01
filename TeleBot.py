import telebot
import time
from telebot import types
import requests
import json

bot = telebot.TeleBot('7216008543:AAEvFbjMOwqwLBCg05iiEFD9Podg_GboKms')
API = '9fed8d123df6ddace341afbe55ec3ad3'

joinedFile = open('chatids.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton('Bot information', callback_data = 'bot_info')
    markup.row(button_1)
    button_2 = types.InlineKeyboardButton('Bot functions', callback_data = 'bot_func')
    button_3 = types.InlineKeyboardButton('Functions information', callback_data = 'func_info')
    markup.row(button_2, button_3)
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} <3", reply_markup=markup)
    
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('chatids.txt')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)
    
@bot.message_handler(commands=['letsfgo'])
def letsfgo(message):
    if message.chat.id == 705730918:
        for users in joinedUsers:
            bot.send_message(users, 'RERERERR')
    else:
        bot.send_message(message.chat.id, f'This is admin command! GET OUT!!!@#!~')
        
@bot.message_handler(commands=['dice'])
def dice(message):
    value = bot.send_dice(message.chat.id, '🎲').dice.value
    time.sleep(5)
    bot.send_message(message.chat.id, f'You got: {value}')
        
    
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'bot_info':
            bot.send_message(call.message.chat.id, f'<em><u>Information about this Bot</u></em>\nThe bot was created in order to teach programming bots in telegram. This bot has several useful features that can help in everyday life, as well as some entertaining content', parse_mode='html')
        elif call.data == 'bot_func':
            bot.send_message(call.message.chat.id, f'<em>What can this Bot do?</em>\n1 - <em>Getting the weather</em>', parse_mode='html')
        elif call.data == 'func_info':
            bot.send_message(call.message.chat.id, f'<em><u>Information about Bot functions.</u></em>\n<b>/start</b> - Just launching\n<b>/help</b> - Auxiliary information about the bot\n<b>/weather</b> - Getting the weather in a given city', parse_mode='html')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, f"Oh heLl nAh bruH")
       
@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, f'Enter the name of the city...')
    
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if weather.status_code == 200:
        data = json.loads(weather.text)
        bot.reply_to(message, f'Now {data["main"]["temp"]} degrees in {city}. Feels like {data["main"]["feels_like"]}')
    else:
        bot.reply_to(message, f'Incorrect city. Try again')
    
             
bot.polling(none_stop=True)

