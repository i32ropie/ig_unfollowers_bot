# telegram-bot-template
Este repositorio es una plantilla para crear bots con [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) de forma sencilla y dockerizada.

# Instrucciones
A continuación se describen las instrucciones a seguir para hacer funcionar nuestro bot de Telegram.

Tenemos 2 opciones:
- [Usando Docker](#docker)
- [Usando instalación local de Python](#python)


## Pasos previos

En ambas modalidades, necesitamos previamente crear un bot desde [BotFather](https://telegram.me/botfather) para obtener el TOKEN de nuestro bot.

Una vez tenemos el TOKEN, debemos renombrar el fichero `.env.sample` por `.env` y reemplazar el valor actual de `BOT_TOKEN` con el de nuestro TOKEN.

## Usando Docker <a name="docker"></a>

En caso de usar Docker, podemos construir nuestro bot y ejecutarlo con el siguiente comando:

```bash
docker compose up -d --build
```

Cuando se complete el comando, ya estará ejecutándose nuestro bot. Puedes consultar los logs del mismo mediante el siguiente comando:

```bash
docker compose logs -f
```

## Usando instalación local de Python <a name="python"></a>

Para lanzar nuestro bot usando una instalación local de Python, usaremos un entorno virtual para no ensuciar nuestra instalación local. Los pasos a seguir son los siguientes:

1. [Crear entorno virtual](#crear-venv)
2. [Activar entorno virtual](#activar-venv)
3. [Instalar dependencias](#instalar-dependencias)
4. [Ejecutar bot](#ejecutar-bot)


### Crear entorno virtual <a name="crear-venv"></a>

Cambia `python3` por `python` en caso de necesitarlo:

```bash
python3 -m venv venv
```

### Activar entorno virtual <a name="activar-venv"></a>

Esto dependerá del sistema operativo que estés usando.

En linux/macos será:

```bash
source venv/bin/activate
```

En windows será:

```bat
.\venv\Scripts\activate.bat
```

En ambos casos, si ha funcionado deberíamos ver que nuestro prompt tiene al inicio ahora `(venv)`.

### Instalar dependencias <a name="instalar-dependencias"></a>

Cambia `python3` por `python` en caso de necesitarlo:

```bash
python3 install -r requirements.txt
```

### Ejecutar bot <a name="ejecutar-bot"></a>

Cambia `python3` por `python` en caso de necesitarlo:

```bash
python3 bot.py
```

# Enlaces de interés

- [API de Telegram](https://core.telegram.org/bots/api)