import pygame; from pygame.locals import *


pygame.init()

win = pygame.display.set_mode((800,800))

pic = pygame.image.load("Textures-16.png")
new_pic = pygame.transform.scale(pic, (800, 800))

win.blit(new_pic, (0,0))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    pygame.display.flip()
    
    
