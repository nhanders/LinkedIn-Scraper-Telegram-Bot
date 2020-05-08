# This script will be used for learning the functionality of a Telegram Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
import threading
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import csv

import sys
sys.path.insert(1, '../secret')
import secret

TOKEN = secret.TOKEN

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Error handling
def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        print("Error")
    except BadRequest:
        # handle malformed requests - read more below!
        print("Error")
    except TimedOut:
        # handle slow connection problems
        print("Error")
    except NetworkError:
        # handle other connection problems
        print("Error")
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        print("Error")
    except TelegramError:
        # handle all other telegram related errors
        print("Error")

dispatcher.add_error_handler(error_callback)

# /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# /start command
def getResults(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Getting results...")
    # context.bot.send_document(chat_id=update.effective_chat.id, document=open('csv/results.xlsx', 'rb'))
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('document.csv', 'rb'))


getResults_handler = CommandHandler('getResults', getResults)
dispatcher.add_handler(getResults_handler)

# upload
def upload(update, context):
    file_id = update.message.document.file_id
    newFile = context.bot.get_file(file_id)
    # print(newFile)
    # print(newFile['file_path'])
    newFile.download('document.csv')
    context.bot.send_message(chat_id=update.effective_chat.id, text="File uploaded!")

upload_handler = MessageHandler(Filters.document & (~Filters.command), upload)
dispatcher.add_handler(upload_handler)

# shutdown Bot
def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Terminating Bot...")
    threading.Thread(target=shutdown).start()

updater.dispatcher.add_handler(CommandHandler('stop', stop))

# unknown
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
