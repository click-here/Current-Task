import pygame, sys
from pygame.locals import *
import os  
import time
from db_tool import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# START DB STUFF
engine = create_engine('sqlite:///task.db')
Session = sessionmaker(bind=engine)
session = Session()
last_task = session.query(Task).order_by(Task.id.desc()).first().task_name
# END DB STUFF

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 

clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

pygame.init()
infoObject = pygame.display.Info()
windowSurface = pygame.display.set_mode((infoObject.current_w, 55), pygame.NOFRAME)  

windowSurface.fill(BLACK)
pygame.display.update()

def message_display(text):
    windowSurface.fill(BLACK)
    largeText = pygame.font.Font("segoeui-regular.ttf", 48)
    textSurface = largeText.render(text, True, WHITE)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    
    TextRect.center = (windowSurface.get_rect().centerx,windowSurface.get_rect().centery)
    
    windowSurface.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)
    task_loop()


def task_loop():
    last_task = ''
    time_elapsed_since_last_action = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()         
        
        dt = clock.tick() 

        time_elapsed_since_last_action += dt
        if time_elapsed_since_last_action > 250:
            current_task = session.query(Task).order_by(Task.id.desc()).first().task_name
            print(current_task)
            if last_task != current_task:
                last_task = current_task
                message_display(current_task)
            time_elapsed_since_last_action = 0
            
            
        pygame.display.update()

task_loop()
