# -*- coding: utf-8 -*-
__author__ = 'Denis Titusov, sescusu@gmail.com'

import os
import telebot
import time
from schedule import get_schedule
import botan

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOTAN_TOKEN = os.getenv('BOTAN_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
start_message = """Привет, дружок! Я могу рассказать тебе о ближайших турах Елок Моталок. Если тебе интересно, напиши "туры".
Я пока что совсем маленький и многого не умею, но я учусь!"""


def pretify_schdeule(schedule, user_uuid=None):
    schedule_list = []
    for tour in schedule:
        try:
            tour["shorten_link"] = botan.shorten_url(tour["description"], BOTAN_TOKEN, user_uuid.id)
            tour_string = ("Тур: {name}, едем {date}.\n{shorten_link}").format(**tour)
        except:
            tour_string = ("Тур: {name}, едем {date}.\n{description}").format(**tour)
        finally:
            schedule_list.append(tour_string)
    return schedule_list

@bot.message_handler(commands=["start", "help"])
def start_and_help(message):
    response_markup = telebot.types.ReplyKeyboardMarkup()
    response_markup.add("Туры")
    bot.send_message(message.chat.id, start_message, reply_markup=response_markup)
    botan.track(BOTAN_TOKEN, message.from_user, message, "Start")


@bot.message_handler(regexp=".*(?i)(туры|tour).*")
def send_tour_info(message):
    hider = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.chat.id, 'Сейчас подумаю...', reply_markup=hider)
    botan.track(BOTAN_TOKEN, message.from_user, message, "Tours")
    schedule = get_schedule()
    if not schedule:
        bot.send_message(message.chat.id, "Кажется, какой-то жулик украл все наше расписание. Но мы его уже ищем!")
        return
    pretty_messages = pretify_schdeule(schedule, message.from_user)
    bot.send_message(message.chat.id, "Наши ближайшие туры:\n====================")
    for sch in pretty_messages:
        bot.send_message(message.chat.id, '{0}\n----'.format(sch))
        time.sleep(2)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, ("Извини, я не распознал эту команду.\n"
                                      "Попробуй спросить меня про туры, я расскажу тебе кое-что интересное 😊"))


if __name__ == '__main__':
    bot.polling(none_stop=True)
