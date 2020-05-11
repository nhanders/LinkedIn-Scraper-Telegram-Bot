
# This script will be used for learning the functionality of a Telegram Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import logging, threading, csv, sys

# import user scripts
from secret import secret
from scripts import scraper_main

# States
START, UPLOAD, PROCESSING, RESULTS = range(4)

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Error handling
def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized as e:
        # remove update.message.chat_id from conversation list
        print("Error:", e)
    except BadRequest as e:
        # handle malformed requests - read more below!
        print("Error:", e)
    except TimedOut as e:
        # handle slow connection problems
        print("Error:", e)
    except NetworkError as e:
        # handle other connection problems
        print("Error:", e)
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        print("Error:", e)
    except TelegramError as e:
        # handle all other telegram related errors
        print("Error:", e)

# /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the LinkedIn Scraper Bot!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload a .csv of your employees in the form: Name, LinkedIn_ID \ne.g. John Smith, john-smith-123")

    return UPLOAD

# upload
def fileUploaded(update, context):
    file_id = update.message.document.file_id
    newFile = context.bot.get_file(file_id)
    newFile.download('documents/inputs/empdetails.csv')
    context.bot.send_message(chat_id=update.effective_chat.id, text="File received!")

    keyboard = [[KeyboardButton("/process")],
                [KeyboardButton("/abort")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard = True)

    update.message.reply_text(
        text="Everything is ready. Click /process to begin extracting data or /abort to return to start screen.",
        reply_markup = reply_markup
    )

    return PROCESSING

# /process command
def process(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Starting data extraction.")
    scraper_main.main(update, context)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Getting results...")
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('documents/outputs/results.xlsx', 'rb'))

    return START

# /abort command
def abort(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Returning to start.")

    return START

# /getResults command
# def getResults(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Getting results...")
#     context.bot.send_document(chat_id=update.effective_chat.id, document=open('documents/outputs/results.xlsx', 'rb'))
#
#     return START

# # shutdown Bot
# def shutdown():
#     updater.stop()
#     updater.is_idle = False
#
# def stop(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Terminating Bot...")
#     threading.Thread(target=shutdown).start()

# unknown
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    # token stored locally
    TOKEN = secret.TOKEN

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Setup conversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START:      [CommandHandler('start', start)],
            UPLOAD:     [MessageHandler(Filters.document & (~Filters.command), fileUploaded)],
            PROCESSING: [CommandHandler('process', process),
                         CommandHandler('abort', abort)] #,
            # RESULTS:    [CommandHandler('getResults', getResults)]
        },
        fallbacks=[CommandHandler('start', start)],
        name="my_conversation",
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # log all errors
    dispatcher.add_error_handler(error_callback)

    # stop bot
    # dispatcher.add_handler(CommandHandler('stop', stop))

    # unknown commands
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # start bot
    updater.start_polling()

    # allow CTRL C to stop running
    updater.idle()

# MAIN ------------------------------------------------------------------------

if __name__ == '__main__':
    main()
