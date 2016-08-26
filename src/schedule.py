# -*- coding: utf-8 -*-
__author__ = 'Denis Titusov, sescusu@gmail.com'

import yaml
import urllib.request
import urllib.error
import os
from shutil import copyfile

cache_dir = 'cache'
schedule_file = '{0}/schedule.yml'.format(cache_dir)


def download_schedule():
    schedule_url = os.getenv('SCHEDULE_URL')
    try:
        file_name, headers = urllib.request.urlretrieve(schedule_url)
    except urllib.error.URLError as e:
        print('could not get file {0}'.format(schedule_url))
        print(e)
        return
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    copyfile(file_name, schedule_file)


def get_schedule():
    download_schedule()
    if not os.path.exists(schedule_file):
        print('Файл потерялся...')
        return None

    with open(schedule_file, 'r') as yml_file:
        schedule_raw = yaml.load(yml_file)

    return schedule_raw["NextTourSchedule"]
