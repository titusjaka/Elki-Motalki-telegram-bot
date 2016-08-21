# -*- coding: utf-8 -*-
__author__ = 'Denis Titusov, sescusu@gmail.com'

import yaml

def get_schedule():
    with open('schedule.yml', 'r') as yml_file:
        schedule_raw = yaml.load(yml_file)

    schedule_start = ("Наши ближайшие туры: \n"
                      "====================\n\n")
    schedule_list = [schedule_start]
    for tour in schedule_raw["NextTourSchedule"]:
        tour_string = ("Тур: {name}, едем {date}.\n"
                       "{link}\n----\n").format(**tour)
        schedule_list.append(tour_string)

    return schedule_list