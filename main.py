#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, Job, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import requests
import json

stazione_partenza=""
stazione_arrivo=""
flag=True

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Ciao!')


def setp(bot, update, args):
    global stazione_partenza
    global flag
    lunarg=len(args)
    chat_id = update.message.chat_id
    if (lunarg>0):
        keyboard=[[]]
        ind=""
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
        if(lungh>0):
            if (lungh==1):
                cit= d[0]['name']
                update.message.reply_text("Citta' salvata: "  + cit)
                stazione_partenza=cit
            else:
                flag=True
                for i in range(0, lungh):
                    cit= d[i]['name']
                    keyboard.append([InlineKeyboardButton(cit, callback_data=cit)])
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Please choose:', reply_markup=reply_markup)
        else:
            update.message.reply_text('Nessuna stazione corrispondente, riprova!')
    else:
        update.message.reply_text('Inserisci un valore valido!')


def seta(bot, update, args):
    global stazione_arrivo
    global flag
    lunarg=len(args)
    chat_id = update.message.chat_id
    if (lunarg>0):
        keyboard=[[]]
        ind=""
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
        if(lungh>0):
            if (lungh==1):
                cit= d[0]['name']
                update.message.reply_text("Citta' salvata: "  + cit)
                stazione_arrivo=cit
            else:
                flag=False
                print("sono qui")
                for i in range(0, lungh):
                    cit= d[i]['name']
                    keyboard.append([InlineKeyboardButton(cit, callback_data=cit)])
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Please choose:', reply_markup=reply_markup)
        else:
            update.message.reply_text('Nessuna stazione corrispondente, riprova!')
    else:
        update.message.reply_text('Inserisci un valore valido!')
        
def cerca(bot,update):
    

def printp(bot, update):
    chat_id = update.message.chat_id
    print(stazione_partenza)
    update.message.reply_text('La tua stazione di partenza e\': ' + stazione_partenza)

def printa(bot, update):
    chat_id = update.message.chat_id
    print(stazione_arrivo)
    update.message.reply_text('La tua stazione di partenza e\': ' + stazione_arrivo)

def button(bot, update):
    global stazione_partenza
    global stazione_arrivo
    global flag
    query = update.callback_query
    print(flag)
    if flag:
        print("p")
        stazione_partenza=query.data
    else:
        print("a")
        stazione_arrivo=query.data
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
    dp.add_handler(CommandHandler("stampap", printp))
    dp.add_handler(CommandHandler("stampaA", printa))
    dp.add_handler(CommandHandler("andata", cerca))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("setp", setp,
                                  pass_args=True))
    dp.add_handler(CommandHandler("seta", seta,
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
    
