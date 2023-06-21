import pygame, sys, time
from pygame.locals import *

RESOLUTION = (960,480)
TEXTURESIZE= (16,16)
OFFSET = 480
FPS = pygame.time.Clock()
window = pygame.display.set_mode(RESOLUTION)

picture = pygame.image.load("Assets//brick1.png")

def scalePicture(x,y,sizeX,sizeY):    
    scaled = pygame.transform.scale(picture, (sizeX,sizeY))
    pygame.Surface.blit(window, scaled,(x,y))
    
def darkenScalePicture(x,y,sizeX,sizeY,dist):
    col = (dist//100)
    if col > 250: col = 250
    scaled = pygame.transform.scale(picture, (sizeX,sizeY))
    scaled.fill((col,col,col),special_flags=pygame.BLEND_SUB)
    pygame.Surface.blit(window, scaled,(x,y))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    scalePicture(0,0,480,480) 
    for i in range(1,5000):
        darkenScalePicture(OFFSET+0,0,480,480,i)
        pygame.display.update()
        #FPS.tick(10)
    pygame.display.update()