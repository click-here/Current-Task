import pygame, sys
from pygame.locals import *
import os  
import time
from db_tool import Task, Water
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Date, cast
from datetime import date

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
GREEN = (255, 0 ,255)

clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

pygame.init()
infoObject = pygame.display.Info()
windowSurface = pygame.display.set_mode((infoObject.current_w, 55), pygame.NOFRAME)  

windowSurface.fill(BLACK)

# water button
pygame.draw.rect(windowSurface, GREEN, [0, 35, 20, 20])

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

def show_water():
##    water_amnt = Water(amount=24)
##    session.add(water_amnt)
##    session.commit()

    daily_amount = session.query(Water).filter(Water.created_date >= date.today())
    daily_amount = sum([x.amount for x in daily_amount])
    daily_goal = 72

    percent_of_daily_goal = daily_amount / daily_goal

    rect_size = infoObject.current_w * percent_of_daily_goal
    print(rect_size)
    pygame.draw.rect(windowSurface, BLUE, [0, 0, rect_size, 5])
    pygame.display.update()




def task_loop():
    last_task = ''
    time_elapsed_since_last_action = 0
    while True:       
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # On right click mark task showing as done.
                if event.button == 3:
                    mark_current_task_done()
                    get_recent_query()
            # If mouse touches top of screen requery the db.
            if pygame.mouse.get_pos()[1] == 0:
                get_recent_query()
                
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()     

        pygame.display.update()

task_loop()
