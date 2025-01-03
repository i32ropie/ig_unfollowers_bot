import os
import zipfile
import json
from io import BytesIO
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
    bot.reply_to(message, "Hola, soy un bot que te dice quién te ha dejado de seguir :) mándame el fichero zip exportado de instagram (habiendo seleccionado formato JSON) y déjame el resto a mi :)")
    bot.send_message(message.chat.id, "Para generar el fichero\n 1. Ve a tu perfil de instagram\n 2. Pulsa en los tres puntos de arriba a la derecha\n 3. Tu actividad\n 4. Descargar tu información (abajo del todo)\n 5. Descargar o transferir información\n 6. Parte de tu información\n 7. Seguidores y seguidos\n 8. Siguiente\n 9. Descargar en el dispositivo\n 10. En intervalo de fechas, seleccionar 'Desde el principio' y guardar\n 11. En formato, seleccionar JSON\n 12. Ahora dale a 'Crear archivos' y espera a que te llegue el fichero")
    bot.send_message(message.chat.id, "Una vez lo tengas, mándamelo y te diré quién de la gente que tú sigues no te sigue de vuelta!\n\nPara encontrar el fichero, tienes que volver a ir al apartado de descargar tu información, y ahí te aparecerá para descargar la información que has pedido")

# Creamos un manejador para los ficheros ZIP con la info de instragram
@bot.message_handler(content_types=['document'])
def echo_message(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    # Comprobamos que el fichero sea un ZIP
    if not file_info.file_path.endswith('.zip'):
        bot.reply_to(message, "Por favor, mándame un fichero ZIP")
        return
    # Comprobamos que el tamaño del fichero sea menor de 20MB
    if file_info.file_size > 20 * 1024 * 1024:
        bot.reply_to(message, "El fichero es demasiado grande, mándame uno más pequeño")
        return
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    bot.reply_to(message, "OK, he recibido el fichero, ahora voy a procesarlo")
    try:
        followers, following = [], {'relationships_following': []}
        # Extraemos el fichero ZIP
        with zipfile.ZipFile(BytesIO(file.content)) as zip_ref:
            # Leemos los ficheros JSON
            try:
                with zip_ref.open('connections/followers_and_following/followers_1.json') as f:
                    followers = json.load(f)
                with zip_ref.open('connections/followers_and_following/following.json') as f:
                    following = json.load(f)
            except:
                bot.reply_to(message, "No he podido procesar el fichero, asegúrate de que es el fichero correcto")
        # Creamos una lista con los nombres de los followers
        a = [x['string_list_data'][0]['value'] for x in followers]
        # Creamos una lista con los nombres de los following
        b = [x['string_list_data'][0]['value'] for x in following['relationships_following']]
        # Creamos una lista con los nombres de los unfollowers
        unfollowers = set(b) - set(a)
        # Enviamos la lista de unfollowers, cada uno en una linea con un - delante para que se vea como una lista, con enlaces a los perfiles de instagram y sin mostrar preview
        bot.send_message(message.chat.id, "\n".join([f"- [{x}](https://www.instagram.com/{x}/)" for x in unfollowers]), parse_mode='Markdown', disable_web_page_preview=True)
    except:
        bot.reply_to(message, "No he podido procesar el fichero, asegúrate de que es el fichero correcto")

# Iniciamos el bot
bot.infinity_polling()