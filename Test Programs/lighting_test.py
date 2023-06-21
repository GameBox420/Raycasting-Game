import os, sys, math, numpy
import pygame
from pygame.locals import *
#pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
RES_H = 320
RES_W = 640
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

class Player():
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
    def move(self,map_id):
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
        if map[map_id][newmy*mapx+newmx]==0:
            self.pos +=self.delt

P1 = Player()

#map data
def readMapData(file_name):
    file = open(file_name, "r")
    data = file.read()
    chars= len(data)
    array = []
    for i in range(0,chars):
        array.append(int(data[i]))
    return array
map = [readMapData("Map1.txt")]
#raycasting variables
FOV = 60 #FOV in degrees.
NOR = int(RES_W/16) #the number of rays cast
Rays_Per_Radian = NOR/FOV #how many rays in 1 radian
inc = DR/Rays_Per_Radian #angle to increment the rays by each iteration
width = RES_W/NOR #width of each ray once its drawn on the screen
#horizon = RES_H/2 #initial y-position on the screen to draw from.
if mapx > mapy:maxdof = mapx  #this optimizes the max number of calculations to the maximum you would need to cast a ray
else          :maxdof = mapy  #along the longest side of the map.
maxDistance = maxdof*blockRes #the farthest a ray can possibly be
blkDistance = 250 #the farthest a ray can be before it is drawn all black
#textures
path = "Assets/"
textures = [
    #pygame.image.load("skybox.png"),
    pygame.image.load(path+"sky.png"), #since 0 is air in the raycasting algorithm, this address can be used for blank or testing pictures.
    pygame.image.load(path+"stone.png"),
    pygame.image.load(path+"stonebrick.png"),
]  
# The rays are drawn using the data calculated by the raycast() function. Each map grid is split into a 16x16 square.
# Firstly, texpos is calculated. Texpos is the collum of the 16x16 wall that the ray hit. Next, take the coresponding texture for the wall
# and copy the collumn number texPos. The scale the slice of the texture to width, which is how many collumns the screen is split in
# Finally, the slice is tinted based on distance for lighting.
def drawRay(r,posx, posy,height,offset,distance,orientation, texture = pygame.Surface):
    slice = pygame.Surface((1, blockRes))
    if orientation == "horizontal": #wall is horizontal, x decides texture pos
        texPos = (posx % blockRes)
    if orientation == "vertical": #wall is verical, y decides texture pos
        texPos = (posy % blockRes)
    slice.blit(texture,(0,0),(texPos,1,1,blockRes))#gets a 1xblockRes slice of the texture to draw
    ray = pygame.transform.scale(slice,(width, height))
    if distance > blkDistance:
        col = 255
    else:
        col = 255/(int(blkDistance/distance)+1)
    if col > 255: col = 255
    ray.fill((col,col,col),special_flags=pygame.BLEND_SUB)
    pygame.Surface.blit(win, ray,((r*width),offset))
    #draw floor
#
def raycast(map_id) :
    ra = P1.angle - PI/6
    for r in range(NOR):
        #re-init variables for new iteration
        if ra > 2*PI: ra -=2*PI
        if ra < 0   : ra +=2*PI
        dof=0
        hx,vx = P1.pos.x,P1.pos.x
        hy,vy = P1.pos.y,P1.pos.y
        dish,disv = float(1000000),float(1000000)
        nTan= -(math.tan(ra));aTan=-1/math.tan(ra)
        #check horizontal lines
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
            if mp > 0 and mp < mapx * mapy and map[map_id][mp]>0 :
                dof = maxdof
                hx = rx
                hy = ry
                dish = math.dist((hx, hy), (P1.pos.x, P1.pos.y))
                htex = map[map_id][mp]
            else :
                rx += xo
                ry += yo
                dof += 1
        #check vertical lines
        dof=0
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
            if mp > 0 and mp < mapx * mapy and map[map_id][mp]>0 :
                dof = maxdof
                vx = rx
                vy = ry
                disv = math.dist((rx, ry), (P1.pos.x,P1.pos.y))
                vtex = map[map_id][mp]
            else :
                rx += xo
                ry += yo
                dof += 1
        #compare lines
        if disv<dish :
            rx,ry,disT = vx,vy,disv
            orientation = "vertical"
            tex = vtex
        if disv>dish :
            rx,ry,disT = hx,hy,dish
            orientation = "horizontal"
            tex = htex
            
        #disT *=  math.cos(math.radians(P1.angle-ra)) #fisheye correction
        lineH = (blockRes * RES_H)/disT * math.cos(math.radians(P1.angle-ra))
        if lineH > 5000: lineH = 5000 #limit the line size to fix problem with pygame.transform.scale() absolutely tanking performance.
        lineO = P1.horizon - lineH/2
        drawRay(r,rx,ry,lineH,lineO,disT,orientation,textures[tex])
        #increment angle for next iteration
        ra += inc
#
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    #win.fill((0,0,0))
    win.fill('black');pygame.draw.rect(win,(25,25,25),(0,P1.horizon,RES_W,RES_H))#draws sky and temporary floor
    pygame.draw.arc(win,(40,40,40),(0,P1.horizon,RES_W,RES_H),PI/3,PI/3) #draw vignette
    P1.move(0)
    raycast(0)
    cursor = pygame.Rect(RES_W/2,RES_H/2,4,4)
    pygame.draw.rect(win,(255,0,0),cursor)
    pygame.display.flip()
    FramePerSec.tick(FPS)
    pygame.display.set_caption("Raycaster    FPS: " + str(int(FramePerSec.get_fps()))) #get fps, round it with int(), string it with str()