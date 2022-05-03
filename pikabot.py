#!/usr/bin/env python

import logging
import random
import os
import sys
import re

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

import giphy_client


logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

#####################
try:
    TOKEN = os.environ['TG_TOKEN']
    GIPHY_TOKEN = os.environ['G_TOKEN']
except KeyError:
    logging.error('Please make sure to pass both Telegram API token (TG_TOKEN) and Giphy API token (G_TOKEN) as environmental variables!')
    sys.exit(1)

STICKER_PACK = 'MrAss'
STICKER_ID = 'AgADHhEAAixS0Ek'
GIPHY_LIMIT = 25
YUGE_ID = 'l0HefZY0mFfLS9AFa'
YUGE_REGEX = re.compile(r'[h|y]u+ge', re.IGNORECASE)
JEFF_REGEX = re.compile(r'jeff|bezos', re.IGNORECASE)
#####################


updater = Updater(token = TOKEN, use_context = True)
dispatcher = updater.dispatcher

api_instance = giphy_client.DefaultApi()


def grab_random_pika_gif():
    api_response = api_instance.gifs_search_get(GIPHY_TOKEN, 'pikachu', limit = GIPHY_LIMIT)
    url = api_response.data[random.randrange(GIPHY_LIMIT)].images.downsized_small.mp4
    logging.info(f'Grabbed random pika image: {url}')
    return url

def reply_to_pika(update: Update, context: CallbackContext):
    if update.message.sticker.set_name == STICKER_PACK and update.message.sticker.file_unique_id == STICKER_ID:
        logging.info(f'Got a morning ass from {update.message.chat.first_name}[{update.message.chat.id}]')
        pika = grab_random_pika_gif()
        context.bot.send_animation(chat_id = update.effective_chat.id, animation = pika)
        logging.info('Pika gif sent to chat.')

morning_handler = MessageHandler(Filters.sticker, reply_to_pika)
dispatcher.add_handler(morning_handler)


def send_yuge(update: Update, context: CallbackContext):
    api_response = api_instance.gifs_gif_id_get(GIPHY_TOKEN, YUGE_ID)
    url = api_response.data.images.downsized_small.mp4
    context.bot.send_animation(chat_id = update.effective_chat.id, animation = url)
    logging.info('Yuge gif sent to chat.')

yuge_handler = MessageHandler(Filters.text & Filters.regex(YUGE_REGEX), send_yuge)
dispatcher.add_handler(yuge_handler)


def grab_random_jeff_gif():
    api_response = api_instance.gifs_search_get(GIPHY_TOKEN, 'bezos', limit = GIPHY_LIMIT)
    url = api_response.data[random.randrange(GIPHY_LIMIT)].images.downsized_small.mp4
    logging.info(f'Grabbed random Jeff image: {url}')
    return url

def send_jeff(update: Update, context: CallbackContext):
    jeff = grab_random_jeff_gif()
    context.bot.send_animation(chat_id = update.effective_chat.id, animation = jeff)
    logging.info('Jeff gif sent to chat.')


jeff_handler = MessageHandler(Filters.text & Filters.regex(JEFF_REGEX), send_jeff)
dispatcher.add_handler(jeff_handler)

updater.start_polling()
updater.idle()
