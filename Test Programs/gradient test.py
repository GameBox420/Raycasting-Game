import pygame,sys,math
from pygame.locals import *
RESOLUTION = (640,320)

win = pygame.display.set_mode(RESOLUTION)



def draw():
    pygame.draw.circle(win,())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    win.fill(255,255,255)
    
    draw()