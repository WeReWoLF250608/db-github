import os
from pymongo import MongoClient
import pymongo
from flask import Flask, request
from telebot import types
import random
import telebot

TOKEN = "5220542900:AAHZCYn3vr5G-RDLJ7ExEFbU34FIUlm4sB0"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


# Вводим ссылку на подключение (не забудьте поменять имя пользователя и пароль!)
CONNECTION_STRING = "mongodb+srv://WEREWOLF_YT:WeReWoLF25062008@cluster0.lucx4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Подключаемся к аккаунту
client = MongoClient(CONNECTION_STRING)

# Создаём базу данных (название указано в кавычках)
db = client['first_DB'] # first_DB - название базы данных

collection_items = db["items"] # создаём коллекцию
collection_games = db["Games"] # создаём коллекцию
collection_films = db["Films"]

@bot.message_handler(commands=['start'])
def welcome(message):
  k=types.ReplyKeyboardMarkup()
  k.add('/FILMs')
  k.add('/randfilms')
  bot.send_message(message.chat.id, 'Привет, вот перечень всех команд:', reply_markup=k)

@bot.message_handler(content_types=['text']) 
def start(message):
  if message.text == '/FILMs':
    films = collection_films.find()
    for film in films:
      bot.send_message(message.chat.id, film["Название"])
   
  elif message.text == '/randfilms':
    films = collection_films.find()
    f=[]
    for i in films:
      f.append(i)
    rfilm = random.choice(f)
    bot.send_message(message.chat.id, rfilm["Название"])

  elif message.text == "/filmByGenre":
    print(123)



@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
    
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dbandgit.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
