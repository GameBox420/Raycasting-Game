import sys,math
import pygame;from pygame.locals import *; pygame.init() #get pygame ready
import config,editor #import the other project programs
from config import *



class Player():
    def __init__(self):
        super().__init__()
        self.surface_size = pygame.math.Vector2(15,15)
        self.surface = pygame.Surface(self.surface_size)
        self.pos = pygame.math.Vector2((2*blockRes, 2*blockRes))
        self.delt = pygame.math.Vector2(0,0)
        self.angle = float(1)
        self.rect = self.surface.get_rect(center = self.pos)
        self.facing = pygame.math.Vector2(0, 0)
        self.delt = pygame.math.Vector2(math.cos(self.pos.x), math.cos(self.pos.y))
        self.horizon = RES_H/2
    def move(self,map_id):
        pressed_keys = pygame.key.get_pressed()
        self.delt *=0
        if pressed_keys[K_RIGHT]:
            self.angle += 0.1
            if self.angle > 2 * PI :
                self.angle -= 2 * PI
            #self.delt= pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle)) 
        if pressed_keys[K_LEFT]:
            self.angle -= 0.1
            if self.angle < 0 :
                self.angle += 2 * PI
            #self.delt= pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))    
        if pressed_keys[K_UP] and self.horizon < RES_H:
            self.horizon +=10
        if pressed_keys[K_DOWN] and self.horizon > 0:
            self.horizon -=10
        
        if pressed_keys[K_d]:
            self.delt= pygame.math.Vector2(math.cos(self.angle+PI/2), math.sin(self.angle+PI/2))
            #self.pos += self.delt # type: ignore
            
        if pressed_keys[K_a]:
            self.delt= pygame.math.Vector2(math.cos(self.angle-PI/2), math.sin(self.angle-PI/2))
            #self.pos += self.delt # type: ignore

        if pressed_keys[K_s]:
            self.delt= pygame.math.Vector2(-math.cos(self.angle), -math.sin(self.angle))
            #self.pos -= self.delt # type: ignore

        if pressed_keys[K_w]:
            self.delt= pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))
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

def readMapData(file_name):
    file = open(file_name, "r")
    data = file.read()
    chars= len(data)
    array = []
    for i in range(0,chars):
        array.append(int(data[i]))
    return array



#map = [readMapData("Map1.txt")]

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
    ray = pygame.transform.scale(slice,(width, height)) #scale the slice to the width it will take up, and a height calculated using the length of the ray. (Longer -> Shorter)
    if distance > blkDistance:col = 255 #if the distance is greater than blkDistance, the wall is shaded entirely black
    else:col = 255/(int(blkDistance/distance)+1) #if it isnt, use the tinting formula that was developed in darkening algorithm.py
    if col > 255: col = 255 #if color is greater than 255, it will produce an error, so cap it at 255
    ray.fill((col,col,col),special_flags=pygame.BLEND_SUB)#this tints the picture using the values calculated earlier
    pygame.Surface.blit(win, ray,((r*width),offset))#print to screen
    #draw floor
#
def raycast(map_id) :
    ra = P1.angle - PI/6 #set the initial angle to 30 degress to the left of the player's angle. this is because the game is 60 deg FOV.
                         #this will then make rays in a 60 deg fan shape with the players angle being the center
                         
                         
    #The raycasting algorithm involves casting a "ray" from a starting point at a pre-defined angle. It is used commonly for things like hit detection
    #and checking for intersections between an object and another object's ray.
    #This raycasting algorithm uses DDA, or digital differential analyzer. DDA is used to find multiple intersection points of a line
    #traveling on a grid. DDA is so exceptionally fast because it calculates an offset, which is used to increment lines to the exact
    #next interesection point of the ray. This drastically decreases the number of checks made in comparison to the original algorithm I used
    #which simple incremented the ray by the sine and cosine of the ray's angle. Essentially, the function runs in a structure like this:
    #
    # The player is on a map made up of a grid of 1 unit by 1 unit square tiles. The map contains data on each tile, with a 0 being air,
    # that does not interact with rays, and numbers over 0, which do interact with rays.
    #
    # Initialize a ray from angle RA
    # check horizontal grid lines using an algorithm:
    #   check current ray position for wall:
    #       if there isn't one, increment the ray by its offset.
    #       if there is, stop the algorithm and save the ending position of the ray, including; position, value of wall hit, number of
    #       checks to intersect, angle, and distance between starting position and final ray position.
    # intialize another ray from the same angle RA
    # check vertical grid lines using the same algorithm, the difference here is the value of the offset.
    # Imagining each ray as a line coming from your eye, the shortest of the rays will be the one you actually see, so each ray is compared
    # and data from the shorter ray is saved.
    # The data from the ray is passed to the drawRay() function.
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
            ry = (int(P1.pos.y / blockRes)) * blockRes + blockRes;rx = (P1.pos.y - ry) * aTan + P1.pos.x;yo = blockRes;xo = -yo * aTan
        if ra == 0 or ra == PI : #facing parrellel to x axis
            rx = P1.pos.x;ry = P1.pos.y;dof = maxdof
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
            
        disT *=  math.cos(math.radians(P1.angle-ra)) #fisheye correction
        lineH = (blockRes * RES_H)/disT #calculate the height of the wall depending on distance
        if lineH > 5000: lineH = 5000 #limit the line size to fix problem with pygame.transform.scale() absolutely tanking performance.
        lineO = P1.horizon - lineH/2 #calculate how far from the horizon the line needs to be drawn
        drawRay(r,rx,ry,lineH,lineO,disT,orientation,textures[tex])
        #increment angle for next iteration
        ra += inc
#


map = [readMapData("Map1.txt")]

def runLevel():
    win = pygame.display.set_mode((RES_W, RES_H))
    running = True
    while running:
        for event in pygame.event.get(): #gathers all events pygame detects, events are mostly just the user interacting with the program window or keyboard
            if event.type == QUIT: #quit event is clicking the X on the program window
                running = False
            if event.type == KEYDOWN: #if event is a pressed key, check if the key is escape. if it is, exit the program
                if event.key == K_ESCAPE:
                    running = False
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
        
        
runLevel()
pygame.quit()
sys.exit()