from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import config as cfg
# Contains all handlers
from handlers import handlers

# Logging errors/messages, if any
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


# This continuously fetches updates from telegram
updater = Updater(token=cfg.keys['access_token'])
dispatcher = updater.dispatcher


# Starting conversation with the bot
start_handler = CommandHandler(command='start', callback=handlers.start)
dispatcher.add_handler(start_handler)

# Get meaning handler
dict_handler = CommandHandler('dict', handlers.get_meaning)
dispatcher.add_handler(dict_handler)

# Handling unknown commands
unknown_command_handler = MessageHandler(Filters.command, handlers.unknown)
dispatcher.add_handler(unknown_command_handler)


# Initiating the bot
updater.start_polling()
