import os, sys, math, numpy
import pygame
from pygame.locals import *
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
RES_H = 720
RES_W = 1280
ACC = 1
FPS = 60
PI = math.pi;P2 = PI/2;P3 = 3*PI/2;DR = 0.0174533
FramePerSec = pygame.time.Clock()
win = pygame.display.set_mode((RES_W, RES_H))
pygame.mouse.set_visible(False)
#raycasting variables
mapx, mapy= 20, 20
blockRes = 64
map_2_raycast = 480/(blockRes * mapx)
map1 = [
2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,
2,0,0,0,2,2,0,0,0,2,0,0,0,0,1,0,0,0,0,1,
2,0,0,0,2,2,0,0,0,2,0,0,0,0,0,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,1,
2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,
2,2,2,2,2,2,2,2,2,2,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
]
#init player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface_size = vec(15,15)
        self.surface = pygame.Surface(self.surface_size)
        self.pos = vec((2*blockRes, 2*blockRes))
        self.delt = vec(0,0)
        self.angle = float(1)
        self.rect = self.surface.get_rect(center = self.pos)
        self.facing = vec(0, 0)
        self.delt = vec(math.cos(self.pos.x), math.cos(self.pos.y))
        self.horizon = RES_H/2
    def move(self):
        

        pressed_keys = pygame.key.get_pressed()
        self.delt *=0
        
        if pressed_keys[K_RIGHT]:
            self.angle += 0.1
            if self.angle > 2 * PI :
                self.angle -= 2 * PI
            #self.delt= vec(math.cos(self.angle), math.sin(self.angle))
            
        if pressed_keys[K_LEFT]:
            self.angle -= 0.1
            if self.angle < 0 :
                self.angle += 2 * PI
            #self.delt= vec(math.cos(self.angle), math.sin(self.angle))
            
        if pressed_keys[K_UP] and self.horizon < RES_H:
            self.horizon +=10
        if pressed_keys[K_DOWN] and self.horizon > 0:
            self.horizon -=10
        
        if pressed_keys[K_d]:
            self.delt= vec(math.cos(self.angle+PI/2), math.sin(self.angle+PI/2))
            #self.pos += self.delt # type: ignore
            
        if pressed_keys[K_a]:
            self.delt= vec(math.cos(self.angle-PI/2), math.sin(self.angle-PI/2))
            #self.pos += self.delt # type: ignore

        if pressed_keys[K_s]:
            self.delt= vec(-math.cos(self.angle), -math.sin(self.angle))
            #self.pos -= self.delt # type: ignore

        if pressed_keys[K_w]:
            self.delt= vec(math.cos(self.angle), math.sin(self.angle))
            #self.pos += self.delt # type: ignore
            
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
        
        self.delt *= 5
        newmx, newmy = int((self.pos.x+self.delt.x)/blockRes),int((self.pos.y+self.delt.y)/blockRes)
        if map1[newmy*mapx+newmx]==0:
            self.pos +=self.delt


    def draw(self):
        self.rect = self.surface.get_rect(center = (self.pos))
        #pygame.draw.rect(map2D, (0, 0, 0), self.rect)
        self.mapPos = vec(self.pos.x/mapx,self.pos.y/mapy)
        self.facing = self.pos + (vec(self.delt)*10) 
        pygame.draw.line(map2D, (0 ,0, 250), self.pos, self.facing, 5)
        map2D.blit(self.surface, self.pos - (self.surface_size/2))
        #pygame.display.flip
        pygame.Surface.blit(self.surface, map2D,(self.mapPos))
P1 = Player()
#raycasting variables
FOV = 60 #FOV in degrees.
NOR = int(RES_W/8) #the number of rays cast
Rays_Per_Radian = NOR/FOV #how many rays in 1 radian
inc = DR/Rays_Per_Radian #angle to increment the rays by each iteration
width = RES_W/NOR #width of each ray once its drawn on the screen
maxLineSize = 500
#horizon = RES_H/2 #initial y-position on the screen to draw from.
if mapx > mapy:maxdof = mapx  #this optimizes the max number of calculations to the maximum you would need to cast a ray
else          :maxdof = mapy  #along the longest side of the map.

#textures
path = "Assets/"
textures = [
    #pygame.image.load("skybox.png"),
    pygame.image.load(path+"sky.png"), #since 0 is air in the raycasting algorithm, this address can be used for the skybox.
    pygame.image.load(path+"stone.png"),
    pygame.image.load(path+"stonebrick.png"),
]  
def drawRay(r, posx, posy, height,offset, orientation, texture = pygame.Surface):
    slice = pygame.Surface((1, blockRes))
    if orientation == "horizontal": #wall is horizontal, x decides texture pos
        texPos = (posx % blockRes)
    if orientation == "vertical": #wall is verical, y decides texture pos
        texPos = (posy % blockRes)
    slice.blit(texture,(0,0),(texPos,1,1,blockRes))#gets a 1xblockRes slice of the texture to draw
    ray = pygame.transform.scale(slice,(width, height))
    pygame.Surface.blit(win, ray,((r*width),offset))
    #draw floor
      
def raycast() :
    global r; global mx; global my; global mp; global dof;global rx; global ry; global ra; global xo; global yo; global disT;global ra; global pa #thanks python
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
            ry = (int(P1.pos.y / blockRes)) * blockRes - 0.0001 #determine initial collision between player position and the grid the player in in.
            rx = (P1.pos.y - ry) * aTan + P1.pos.x
            yo =-blockRes
            xo = -yo * aTan
        if ra < PI : #facing downwards
            ry = (int(P1.pos.y / blockRes)) * blockRes + blockRes
            rx = (P1.pos.y - ry) * aTan + P1.pos.x
            yo = blockRes
            xo = -yo * aTan
        if ra == 0 or ra == PI : #facing parrellel to x axis
            rx = P1.pos.x
            ry = P1.pos.y
            dof = maxdof
        while dof < maxdof :
            mx = int(rx / blockRes)
            my = int(ry / blockRes)
            mp = my * mapx + mx
            if mp > 0 and mp < mapx * mapy and map1[mp]>0 :
                dof = maxdof
                hx = rx
                hy = ry
                dish = math.dist((hx, hy), (P1.pos.x, P1.pos.y))
                htex = map1[mp]
            else :
                rx += xo
                ry += yo
                dof += 1
        #    check vertical lines
        dof=0
        disv = float(1000000)
        vx = P1.pos.x
        vy = P1.pos.y
        nTan= -(math.tan(ra))
        if ra > P2 and ra < P3 :
            rx = (int(P1.pos.x / blockRes)) * blockRes - 0.0001
            ry = (P1.pos.x - rx) * nTan + P1.pos.y
            xo =-blockRes
            yo = -xo * nTan
        if ra < P2 or ra > P3 :
            rx = (int(P1.pos.x / blockRes)) * blockRes + blockRes
            ry = (P1.pos.x - rx) * nTan + P1.pos.y
            xo = blockRes
            yo = -xo * nTan
        if ra == 0 or ra == PI :
            ry = P1.pos.y
            rx = P1.pos.x
            dof = maxdof
        while dof < maxdof :
            mx = int(rx / blockRes)
            if mx >= blockRes :
                mx = blockRes-1
            my = int(ry / blockRes)
            if my >= blockRes :
                my = blockRes-1
            mp = my * mapx + mx
            if mp > 0 and mp < mapx * mapy and map1[mp]>0 :
                dof = maxdof
                vx = rx
                vy = ry
                disv = math.dist((rx, ry), (P1.pos.x,P1.pos.y))
                vtex = map1[mp]
            else :
                rx += xo
                ry += yo
                dof += 1
        #compare lines
        if disv<dish :
            rx,ry,disT= vx,vy,disv
            orientation = "vertical"
            tex = vtex
        if disv>dish :
            rx,ry,disT = hx,hy,dish
            orientation = "horizontal"
            tex = htex
        ca = (P1.angle - ra)
        disT *=  math.cos(math.radians(ca)) #fisheye correction
        lineH = (blockRes * RES_H)/disT
        if lineH > 5000: lineH = 5000 #limit the line size to fix problem with pygame.transform.scale() absolutely tanking performance.
        lineO = P1.horizon - lineH/2
        #pygame.draw.line(win, ('dark blue') , (r * width, lineO),(r*width, lineO + lineH),int(width)) #type: ignore #untextured
        drawRay(r,rx,ry,lineH,lineO,orientation,textures[tex])
        
        ra += inc
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
    win.fill('sky blue')
    #pygame.Surface.blit(win, textures[0], (0,0))
    pygame.draw.rect(win,('dark green'),(0,P1.horizon,RES_W,RES_H))#draws sky and temporary floor
    P1.move()
    raycast()
    cursor = pygame.Rect(RES_W/2,RES_H/2,4,4)
    pygame.draw.rect(win,(255,0,0),cursor)
    pygame.display.flip()
    FramePerSec.tick(FPS)
    pygame.display.set_caption("Raycaster    FPS: " + str(int(FramePerSec.get_fps()))) #get fps, round it with int(), string it with str()