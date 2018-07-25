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


clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'


# set up pygame
pygame.init()

# set up the window
infoObject = pygame.display.Info()
windowSurface= pygame.display.set_mode((infoObject.current_w, 55), pygame.NOFRAME)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# set up the text
text = basicFont.render(last_task, True, WHITE)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

# fill background
windowSurface.fill(BLACK)
# draw the text onto the surface
windowSurface.blit(text, textRect)
# draw the window onto the screen
pygame.display.update()


##def text_objects(text, font):
##    textSurface = font.render(text, True, WHITE)
##    return textSurface, textSurface.get_rect()

def message_display(text):
    windowSurface.fill(BLACK)
    largeText = pygame.font.Font('freesansbold.ttf',48)
    textSurface = largeText.render("hrh'", True, WHITE)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    
    TextRect.center = (textRect.centerx,textRect.centery)
    
    windowSurface.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
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
        # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
        if time_elapsed_since_last_action > 250:
            ## I should only call this if a new task is found. will resolve the recursive failure.
            current_task = session.query(Task).order_by(Task.id.desc()).first().task_name
            if last_task != current_task:
                current_task = last_task
                message_display(current_task)
            time_elapsed_since_last_action = 0 # reset it to 0 so you can count again
            
            
        pygame.display.update()

task_loop()
