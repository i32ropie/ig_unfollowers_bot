import os
from dotenv import load_dotenv
import telebot

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la variable de entorno 'BOT_TOKEN'
token = os.getenv('BOT_TOKEN')

# Creamos una instancia del bot
bot = telebot.TeleBot(token)

# Definimos el comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, soy un bot de prueba")

# Creamos un manejador para los mensajes de texto
@bot.message_handler(types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

# Creamos un listener para imprimir los mensajes recibidos
def listener(messages):
    for m in messages:
        print(f"ID: {m.chat.id} - {m.chat.first_name} {m.chat.last_name}: {m.text}")

# Asignamos el listener al bot
bot.set_update_listener(listener)

# Iniciamos el bot
bot.infinity_polling()