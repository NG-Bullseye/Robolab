from pprint import pprint
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging
import time, threading, pickle


TOKEN = '585021350:AAEciXskrmka0wp1xejUsi792YFLiTcg_xY'
updater = Updater(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def key_menu(bot, update):

    text = "Some really long text I\n want on two rows :D"
    callback = "nothing"

    keyboard = []
    keyboard.append([InlineKeyboardButton(text, callback_data = callback)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Some text', reply_markup=reply_markup)

key_menu_handler = CommandHandler('key', key_menu, pass_args=False)
dispatcher.add_handler(key_menu_handler)


updater.start_polling()