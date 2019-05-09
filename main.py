#!/usr/bin/env python
import pygame, sys
from pygame.locals import *
import os, time
from db_tool import Task, Water
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Date, cast
from datetime import date, timedelta, datetime
import subprocess

PYGAME_HEIGHT = 55

### Launch DesktopCoral
## Doesn't work yet, script won't continue until DesktopCoral returns
##os.system("C:\Scripts\DesktopCoral\DesktopCoral.exe -monitorid 1 -placement top -dockheight " + str(PYGAME_HEIGHT))


# START DB STUFF
engine = create_engine('sqlite:///task.db')
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(Task).filter(Task.is_active==1).order_by(Task.id.desc()).first()

if query is not None:
    last_task = query.task_name
else:
    last_task = "No open tasks"
# END DB STUFF

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
BLUE = (0, 255, 255)
RED  = (255,0,0)
YELLOW = (244, 232, 66)

PROG_BAR = pygame.USEREVENT+1

daily_hour_goal = 8.5

clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

pygame.init()
infoObject = pygame.display.Info()
print(pygame.display.Info())
windowSurface = pygame.display.set_mode((infoObject.current_w, PYGAME_HEIGHT), pygame.NOFRAME)  

windowSurface.fill(BLACK)



pygame.display.update()


def message_display(text):
    windowSurface.fill(BLACK)
    largeText = pygame.font.Font("segoeui-regular.ttf", 48)
    textSurface = largeText.render(text, True, WHITE)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    
    TextRect.center = (windowSurface.get_rect().centerx,windowSurface.get_rect().centery)
    
    windowSurface.blit(TextSurf, TextRect)
    show_water()
    pygame.display.update()
    time.sleep(1)
    task_loop()


def get_recent_query():
    current_task = session.query(Task).filter(Task.is_active==1).order_by(Task.id.desc()).first()
    message_display(current_task.task_name)
    time.sleep(2)

def mark_current_task_done():
    
    current_task = session.query(Task).filter(Task.is_active==1).order_by(Task.id.desc()).first()
    
    print(current_task)
    current_task.is_active = 0
    session.commit()
    print('"%s" marked complete'%current_task.task_name)

def add_water():
    water_amnt = Water(amount=24)
    session.add(water_amnt)
    session.commit()
    show_water()

def get_day_start():
    ## I should really have this be a constant or something
    ## Otherwise I'm hitting the DB every second or so via the daily_prog_bar() event trigger
    day_start = session.query(Task).filter(Task.created_date>=date.today()).order_by(Task.id.asc()).first().created_date
    return day_start
 
def show_water():
    # water button
    pygame.draw.rect(windowSurface, YELLOW, [0, 35, 200, 20])
    
    daily_amount = session.query(Water).filter(Water.created_date >= date.today())
    daily_amount = sum([x.amount for x in daily_amount])
    daily_goal = 72

    percent_of_daily_goal = daily_amount / daily_goal

    rect_size = infoObject.current_w * percent_of_daily_goal
    print(rect_size)
    pygame.draw.rect(windowSurface, BLUE, [0, 0, rect_size, 3])
    pygame.display.update()

def convert_to_time(dtime):
    return time.mktime(dtime.timetuple()) + dtime.microsecond / 1E6


def daily_prog_bar():
    daily_start = convert_to_time(get_day_start())
    daily_end = daily_start + 60*60*daily_hour_goal
    cur_time = convert_to_time(datetime.utcnow())
    
    prog_bar = abs((cur_time - daily_start)/(daily_end - daily_start))

    if prog_bar >= 100:
            prog_bar = 100
    elif prog_bar <= 0:
            prog_bar = 0
    return prog_bar

def draw_progres_bar(prog_bar_amnt):
    rect_size = infoObject.current_w * prog_bar_amnt
    pygame.draw.rect(windowSurface, RED, [0, 3, rect_size, 4])
    pygame.display.update()

def task_loop():
    last_task = ''
    pygame.time.set_timer(PROG_BAR, 1000)
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == PROG_BAR:
                print(daily_prog_bar())
                draw_progres_bar(daily_prog_bar())
            if event.type == pygame.MOUSEBUTTONDOWN:
                # On right click mark task showing as done.
                if event.button == 3:
                    mark_current_task_done()
                    get_recent_query()
                if event.button == 1:
                    if 55 >= pygame.mouse.get_pos()[1] >= 35 and 200 >= pygame.mouse.get_pos()[0] >=0: #should clean up this line
                        print(pygame.mouse.get_pos())
                        add_water()
            # If mouse touches top of screen requery the db.
            if pygame.mouse.get_pos()[1] == 0:
                get_recent_query()
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()     

        pygame.display.update()

task_loop()
