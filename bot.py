from pyrogram import Client, idle
from plugins.cb_data import app as Client2
from config import *
import pyrogram.utils
import logging

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Update Pyrogram internal variable
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Initialize Clients
bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root='plugins')
)

if STRING:
    apps = [Client2, bot]
    try:
        for app in apps:
            app.start()
        logging.info("Both clients started.")
        idle()
    except Exception as e:
        logging.error(f"Error during bot operation: {str(e)}")
    finally:
        for app in apps:
            app.stop()
        logging.info("Both clients stopped.")
else:
    try:
        bot.run()
        logging.info("Bot started.")
    except Exception as e:
        logging.error(f"Error during bot operation: {str(e)}")
