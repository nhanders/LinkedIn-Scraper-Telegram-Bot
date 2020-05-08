# This script will be used for learning the functionality of a Telegram Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
import threading
import sys
from secret import secret

TOKEN = secret.TOKEN

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# echo
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# caps
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# shutdown Bot
def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(bot, update):
    threading.Thread(target=shutdown).start()

updater.dispatcher.add_handler(CommandHandler('stop', stop))

# unknown
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

updater.idle()
