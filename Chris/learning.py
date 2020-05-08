# This script will be used for learning the functionality of a Telegram Bot

# My first telegram Bot (chrisTestBot)
# Username: chrisTempBot
# Token: 1283925639:AAFKC0XGVoOl5GbRH5kvorc3eCk9UaJJzpE

# Importing
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import threading

# Creating an Updater object
updater = Updater(token='1283925639:AAFKC0XGVoOl5GbRH5kvorc3eCk9UaJJzpE', use_context=True)
dispatcher = updater.dispatcher

# Setting up logging module to know when things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# function to send a message if command /start given
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! \nI am the PiP LinkedIn Scraper Bot. \nPlease enter '/next' to continue.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def next(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Please enter llist of employee details.")

next_handler = CommandHandler("next", next)
dispatcher.add_handler(next_handler)


# function to echo what is typed
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# shutdown Bot
def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(bot, update):
    threading.Thread(target=shutdown).start()

updater.dispatcher.add_handler(CommandHandler('stop', stop))

# Buttons (https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#build-a-menu-with-buttons)
# def build_menu(buttons,
#                n_cols,
#                header_buttons=None,
#                footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, [header_buttons])
#     if footer_buttons:
#         menu.append([footer_buttons])
#     return menu
#
# button_list = [
#     InlineKeyboardButton("col1", callback_data= ...),
#     InlineKeyboardButton("col2", callback_data=...),
#     InlineKeyboardButton("row 2", callback_data=...)
# ]
# reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
# bot.send_message(..., "A two-column menu", reply_markup=reply_markup)

# Ask for list of employees


# To handle unknown comands
# Has to be after all commands you want to use otherwise those commands don't exist!
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
