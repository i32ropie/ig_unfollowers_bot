import os
import zipfile
import json
import requests
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
    bot.reply_to(message, "Hola, soy un bot que te dice quién te ha dejado de seguir :) mándame el fichero zip exportado de instagram (habiendo seleccionado formato JSON) y déjame el resto a mi")

# Creamos un manejador para los ficheros ZIP con la info de instragram
@bot.message_handler(content_types=['document'])
def echo_message(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    bot.reply_to(message, "OK, he recibido el fichero, ahora voy a procesarlo")
        # Guardamos el fichero en disco con el identificador del chat
    with open(f'followers-{message.chat.id}.zip', 'wb') as f:
        f.write(file.content)
    with zipfile.ZipFile(f'followers-{message.chat.id}.zip', 'r') as zip_ref:
        with zip_ref.open('connections/followers_and_following/followers_1.json') as f:
            followers = json.load(f)
        with zip_ref.open('connections/followers_and_following/following.json') as f:
            following = json.load(f)
    # Creamos una lista con los nombres de los followers
    a = [x['string_list_data'][0]['value'] for x in followers]
    # Creamos una lista con los nombres de los following
    b = [x['string_list_data'][0]['value'] for x in following['relationships_following']]
    # Creamos una lista con los nombres de los unfollowers
    unfollowers = set(b) - set(a)
    # Enviamos la lista de unfollowers, cada uno en una linea con un - delante para que se vea como una lista
    bot.reply_to(message, "\n".join([f"- {x}" for x in unfollowers]))
    # Eliminamos el fichero del disco
    os.remove(f'followers-{message.chat.id}.zip')

# Iniciamos el bot
bot.infinity_polling()