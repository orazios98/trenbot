#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to send timed Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, Job, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import requests
import json


stazione_partenza=""
stazione_arrivo=""

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


def alarm(bot, job):
    """Function to send the alarm message"""
    bot.send_message(job.context, text='Beep!')


def set(bot, update, args):
    """Adds a job to the queue"""
    keyboard=[[]]
    chat_id = update.message.chat_id
    lunarg=len(args)
    ind=""
    print(len(args))
    a1 = args[0]
    ind = 'https://www.lefrecce.it/msite/api/geolocations/locations?name=' + a1
    if(lunarg>1):   
        for i in range(1, lunarg):
            ind= ind+ "%20" + args[i]
    print(ind)
    r = requests.get(ind)
    risp=r.text
    print risp
    d = json.loads(risp)
    lungh=len(d)
    print(lungh)
    if (lungh==1):
        cit= d[0]['name']
        update.message.reply_text("Citta' salvata: "  + cit)
    else:
        for i in range(0, lungh):
            cit= d[i]['name']
            keyboard.append([InlineKeyboardButton(cit, callback_data=cit)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    stazione_partenza=query.data
    print(stazione_partenza)
    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("206255782:AAE2N2fn8q_zvWhV1iaitk5okwPSxsahJyk")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("set", set,
                                  pass_args=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    