import os, sys
import pygame
from pygame.locals import *
import math
import numpy
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

RES_H = 900
RES_W = 1600
ACC = 1
FPS = 120

PI = 3.14159265359
P2 = PI/2
P3 = 3*PI/2
DR = 0.0174533

FramePerSec = pygame.time.Clock()

map2D = pygame.Surface((480,480))
win = pygame.display.set_mode((RES_H, RES_W),pygame.FULLSCREEN,0,0,1)
pygame.mouse.set_visible(False)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface_size = vec(15,15)
        self.surface = pygame.Surface(self.surface_size)
        
        self.pos = vec((2*mapS, 2*mapS))
        self.delt = vec(0,0)
        self.angle = float(1)

        self.rect = self.surface.get_rect(center = self.pos)
        self.facing = vec(0, 0)
        self.delt = vec(math.cos(self.pos.x), math.cos(self.pos.y))
        
        self.horizon = RES_H/2
    def move(self):
        

        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_RIGHT]:
            self.angle += 0.01
            if self.angle > 2 * PI :
                self.angle -= 2 * PI
            self.delt= (math.cos(self.angle), math.sin(self.angle))
            
        if pressed_keys[K_LEFT]:
            self.angle -= 0.01
            if self.angle < 0 :
                self.angle += 2 * PI
            self.delt= (math.cos(self.angle), math.sin(self.angle))
            
        if pressed_keys[K_UP] and horizon < RES_H:
            self.horizon +=10
        if pressed_keys[K_DOWN] and horizon > 0:
            self.horizon -=10
        
        if pressed_keys[K_d]:
            self.delt= (math.cos(self.angle+PI/2), math.sin(self.angle+PI/2))
            self.pos += self.delt # type: ignore
            
        if pressed_keys[K_a]:
            self.delt= (math.cos(self.angle-PI/2), math.sin(self.angle-PI/2))
            self.pos += self.delt # type: ignore

        if pressed_keys[K_s]:
            self.delt= (math.cos(self.angle), math.sin(self.angle))
            self.pos -= self.delt # type: ignore

        if pressed_keys[K_w]:
            self.delt= (math.cos(self.angle), math.sin(self.angle))
            self.pos += self.delt # type: ignore
            
        #mouse camera position
        mousepos = pygame.mouse.get_pos()
        self.looking = (RES_W/2 - mousepos[0], RES_H/2 - mousepos[1])
        pygame.mouse.set_pos(RES_W/2, RES_H/2)
        self.angle += self.looking[0]/-1000
        self.horizon += self.looking[1]
        
        if self.angle > 2 * PI :self.angle -= 2 * PI
        if self.angle < 0 : self.angle += 2 * PI
        
        if self.horizon < 0    : self.horizon = 0
        if self.horizon >RES_H : self.horizon = RES_H
        


    def draw(self):
        self.rect = self.surface.get_rect(center = (self.pos))
        #pygame.draw.rect(map2D, (0, 0, 0), self.rect)
        self.mapPos = vec(self.pos.x/mapx,self.pos.y/mapy)
        self.facing = self.pos + (vec(self.delt)*10) 
        pygame.draw.line(map2D, (0 ,0, 250), self.pos, self.facing, 5)
        map2D.blit(self.surface, self.pos - (self.surface_size/2))
        #pygame.display.flip
        pygame.Surface.blit(self.surface, map2D,(self.mapPos))

'''
mapx, mapy, mapS = 8, 8, 64
map1 = [
1, 1, 1, 1, 1, 1, 1, 1,
1, 0, 0, 0, 1, 0, 0, 1,
1, 0, 1, 0, 1, 0, 0, 1,
1, 0, 0, 0, 1, 0, 0, 1, 
1, 0, 0, 0, 1, 0, 0, 1,
1, 0, 0, 0, 0, 0, 0, 1,
1, 0, 0, 0, 0, 0, 0, 1,
1, 1, 1, 1, 1, 1, 1, 1,]

'''
mapx, mapy= 20, 20
mapS = 64
map1 = [
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
]
map_2_raycast = 480/(mapS * mapx)

def drawmap():
   for x in range(0, mapx):
        for y in range(0, mapy):
            tileO = vec(480/mapx, 480/mapy)
            if map1[y*mapx+x]==1:
                
                tilepos =(x*tileO.x), (y*tileO.y)
                tilecolour = (200, 0, 0)
                tilesize = (480 / mapx, 480/mapy)
                pygame.draw.rect(map2D, tilecolour, Rect(tilepos, tilesize))
            else:
                tilepos =(x*(480/mapx), y*(480/mapy))
                tilecolour = (150, 0, 150)
                tilesize = (480 / mapx, 480/mapy)
                pygame.draw.rect(map2D, tilecolour, Rect(tilepos, tilesize))

P1 = Player()
drawmap()



FOV = 60
NOR = int(RES_W/4)
Rays_Per_Radian = NOR/FOV
inc = DR/Rays_Per_Radian
maxLineSize = 500


#ray casting
r = mx = my = mp = dof = horizon = int(0)
rx = ry = ra = xo = yo = disT = float(0)
ra = pa = P1.angle
maxdof = int

horizon = RES_H/2

if mapx > mapy:
    maxdof = mapx
else:
    maxdof = mapy

def raycast() :
    global r; global mx; global my; global mp; global dof
    global rx; global ry; global ra; global xo; global yo; global disT
    global ra; global pa
    ra = P1.angle - PI/6
    if ra < 0 :
        ra += 2 * PI
    if ra > 2 * PI:
        ra -= 2 * PI
    for r in range(NOR):
        dof=0

        dish = float(100000000)
        hx = P1.pos.x
        hy = P1.pos.y
        
        if ra > 2*PI: ra -=2*PI
        if ra < 0   : ra +=2*PI

        #check horizontal lines
        aTan=-1/math.tan(ra)
        if ra > PI : #facing upwards
            ry = (int(P1.pos.y / mapS)) * mapS - 0.0001 #determine initial collision between player position and the grid the player in in.
            rx = (P1.pos.y - ry) * aTan + P1.pos.x
            yo =-mapS
            xo = -yo * aTan
        if ra < PI : #facing downwards
            ry = (int(P1.pos.y / mapS)) * mapS + mapS
            rx = (P1.pos.y - ry) * aTan + P1.pos.x
            yo = mapS
            xo = -yo * aTan
        if ra == 0 or ra == PI : #facing parrellel to x axis
            rx = P1.pos.x
            ry = P1.pos.y
            dof = 20
        while dof < 20 :
            mx = int(rx / mapS)
            my = int(ry / mapS)
            mp = my * mapx + mx
            if mp > 0 and mp < mapx * mapy and map1[mp] == 1 :
                dof = 20
                hx = rx
                hy = ry
                dish = math.dist((hx, hy), (P1.pos.x, P1.pos.y))
            else :
                rx += xo
                ry += yo
                dof += 1
        ######check vertical lines
        lColor = 255
        dof=0
        disv = float(1000000)
        vx = P1.pos.x
        vy = P1.pos.y
        nTan= -(math.tan(ra))
        if ra > P2 and ra < P3 :
            rx = (int(P1.pos.x / mapS)) * mapS - 0.0001
            ry = (P1.pos.x - rx) * nTan + P1.pos.y
            xo =-mapS
            yo = -xo * nTan
        if ra < P2 or ra > P3 :
            rx = (int(P1.pos.x / mapS)) * mapS + 64
            ry = (P1.pos.x - rx) * nTan + P1.pos.y
            xo = mapS
            yo = -xo * nTan
        if ra == 0 or ra == PI :
            ry = P1.pos.y
            rx = P1.pos.x
            dof = 20
        while dof < 20 :
            mx = int(rx / 64)
            if mx >= 64 :
                mx = 63
            my = int(ry / 64)
            if my >= 64 :
                my = 63
            mp = my * mapx + mx
            
            if mp > 0 and mp < mapx * mapy and map1[mp] == 1 :
                dof = 20
                vx = rx
                vy = ry
                disv = math.dist((rx, ry), (P1.pos.x,P1.pos.y))
            else :
                rx += xo
                ry += yo
                dof += 1
        #compare lines
        if disv<dish :
            rx = vx
            ry = vy
            disT = disv
            lColor = 255
        if disv>dish :
            rx = hx
            ry = hy 
            disT = dish    
            lColor = 230
        
        
        #pygame.draw.line(map2D, (0, 250, 250), (P1.mapPos), (rx/mapx,ry/mapy), 2)
        
        ca = (pa - ra)
               
        disT *=  math.cos(math.radians(ca)) #fisheye correction
        
        lineH = (mapS * RES_H)/disT
        
        #lineH /= disT * math.cos(PI/4)
        
        lineO = P1.horizon - lineH/2
        
        width = RES_W/NOR
        
        
        #lColor = tuple(numpy.subtract(lColor, (shade, shade, shade)))
        
        #print(lColor)
        
        lineCol = (lColor - dof/2, lColor - dof/2 ,lColor - dof/2)
        
        pygame.draw.line(win, lineCol , (r * width, lineO),(r*width, lineO + lineH),int(width)) #type: ignore
        
        '''dir[ray] = direction + arctan((xx / maxfov) * 0.0174533);
            xx += (screen_width / numrays);'''
            
        ra += inc + 0.00000005
            
    P1.facing = P1.pos + (vec(P1.delt)*10)
    pygame.draw.line(map2D, (0 ,0, 250), P1.pos, P1.facing, 5)  
#game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    win.fill((0, 0, 0))
    #drawmap()
    P1.move()
    #P1.draw()
    
    raycast()
    
    cursor = pygame.Rect(RES_W/2,RES_H/2,4,4)
    pygame.draw.rect(win,(255,0,0),cursor)
    
    #pygame.Surface.blit(win, map2D,(0,0)) # type: ignore
    
    pygame.display.update()
    FramePerSec.tick(FPS)
