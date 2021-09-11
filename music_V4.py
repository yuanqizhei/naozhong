import os
import random
from posixpath import dirname
import re
import sys
import time
from datetime import datetime
import pygame
from pygame import font
from pytz import HOUR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup

MUSIC_STOP = pygame.USEREVENT + 1
MUSIC_CONTINUE = pygame.USEREVENT + 2
global STOP

# MUSIC FILE PATH
_dir = os.path.dirname(os.path.abspath(__file__))
playlist_path = os.path.join(_dir,'E:\\Music')
m_list = []
m_play_list = []

# display_width  = 1200
# display_height = 600

screen = pygame.display.set_mode([500,300])

# select the random music file
def random_file():
    rad = random.randint(0,len(m_list)-1)
    print("this time you choose the number",rad)
    print('\n')
    mfile = m_list[rad]
    return mfile

#load the selected file
def load_play_list():
    print('load play list')
    m_list.clear()
    for iroot,idir,flist in os.walk(playlist_path):
        for f in flist:
            if f.find('mp3') != -1:
                m_list.append(os.path.join(iroot,f))
            else:
                print("No mp3")
    
    print(m_list)
    play_music()

#play the music
def play_music():
    print('Music play')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    global STOP
    STOP = 0
    mfile = random_file()
    pygame.mixer_music.load(mfile)
    pygame.mixer_music.play(1)

    while True:
        if STOP == 1:
            break
        elif pygame.mixer_music.get_busy() != 1:
            print('continue the music')
            mfile = random_file()
            pygame.mixer_music.load(mfile)
            pygame.mixer_music.play(1)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mfile = random_file()
                    pygame.mixer_music.load(mfile)
                    pygame.mixer_music.play(1)
                else:
                    break
            else:
                break
#close the music
def stop_music():
    print("stop the music")
    pygame.mixer.music.stop()
    global STOP
    STOP = 1

def main():
    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    #-----------------------------------------------------------------------------------
    #meeting in the moring
    scheduler.add_job(load_play_list,'cron',day_of_week='0-6',hour=7,minute=45,second=0)
    scheduler.add_job(stop_music,'cron',day_of_week='0-6',hour=7,minute=45,second=0)
    
    #have a break in the moring
    scheduler.add_job(load_play_list,'cron',day_of_week='0-6',hour=10,minute=10,second=0)
    scheduler.add_job(stop_music,'cron',day_of_week='0-6',hour=10,minute=20,second=0)

    #lunch time
    scheduler.add_job(load_play_list,'cron',day_of_week='0-6',hour=11,minute=30,second=0)
    scheduler.add_job(stop_music,'cron',day_of_week='0-6',hour=12,minute=0,second=0)

    #work time after noon
    scheduler.add_job(load_play_list,'cron',day_of_week='0-6',hour=12,minute=39,second=0)
    scheduler.add_job(stop_music,'cron',day_of_week='0-6',hour=12,minute=40,second=0)

    #have a break in the afternoon
    scheduler.add_job(load_play_list,'cron',day_of_week='0-6',hour=15,minute=10,second=0)
    scheduler.add_job(stop_music,'cron',day_of_week='0-6',hour=15,minute=20,second=0)

    #work over time
    scheduler.add_job(load_play_list,'cron',day_of_week='0-6',hour=17,minute=0,second=0)
    scheduler.add_job(stop_music,'cron',day_of_week='0-6',hour=17,minute=10,second=0)
    #----------------------------------------------------------------------------------

    print('The process init...')
    pygame.mixer.init()
    pygame.display.flip()

    global STOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # elif event.type == MUSIC_STOP:
            #     print('stop the music')
            # elif event.type == MUSIC_CONTINUE:
            #     print('continue the music')
            #     play_music()
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         play_music()

if __name__ == '__main__':
    print(playlist_path)
    main()


