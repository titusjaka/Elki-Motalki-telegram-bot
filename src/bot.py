# -*- coding: utf-8 -*-
__author__ = 'Denis Titusov, sescusu@gmail.com'

import os
import telebot
import time
from schedule import get_schedule

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
start_message = """Привет, дружок! Я могу рассказать тебе о ближайших турах Елок Моталок. Если тебе интересно, напиши "туры".
Я пока что совсем маленький и многого не умею, но я учусь!"""
schedule = get_schedule()


@bot.message_handler(commands=["start", "help"])
def start_and_help(message):
    response_markup = telebot.types.ReplyKeyboardMarkup()
    response_markup.add("Туры")
    bot.send_message(message.chat.id, start_message, reply_markup=response_markup)


@bot.message_handler(regexp=".*(?i)(туры|tour).*")
def send_tour_info(message):
    hider = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.chat.id, 'Сейчас подумаю...')
    time.sleep(1)
    for sch in schedule:
        bot.send_message(message.chat.id, sch, reply_markup=hider)
        time.sleep(2)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, ("Извини, я не распознал эту команду.\n"
                                      "Попробуй спросить меня про туры, я расскажу тебе кое-что интересное 😊"))


if __name__ == '__main__':
    bot.polling(none_stop=True)
