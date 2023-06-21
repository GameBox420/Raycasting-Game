import pygame, sys,math
from pygame.locals import *
pygame.init()

win = pygame.display.set_mode((940,640))

cursor_pos = pygame.math.Vector2(0,0)
last_keyboard_pos = cursor_pos
clock = pygame.time.Clock()
MAP_BUFFER = 'null' #the map data
DRAW_BUFFER = 'null' #the tile ID currently being drawn

def writeMapData(map, file_name):
    file = open(file_name, "w")
    data = str()
    for i in range(len(map)):
        data += str(map[i])
    file.write(data)
        
def readMapData(file_name):
    file = open(file_name, "r")
    data = file.read()
    chars= len(data)
    array = []
    for i in range(0,chars):
        array.append(int(data[i]))
    if len(array) < 400:
        for i in range(len(array),400):
            array.append(int(0))
    return array

class button:
    def __init__(self,pos,texture):
        self.dimensions = pygame.math.Vector2(64,64)
        self.surface = pygame.Surface(self.dimensions)
        self.position = pygame.math.Vector2(pos)
        self.file = pygame.image.load("Assets/"+texture)
        self.aux = pygame.transform.scale(self.file,self.dimensions)
        self.name = texture
    def blit(self):
        pygame.Surface.blit(win,self.aux,(self.position))
    def getPressed(self, mousePos = pygame.math.Vector2(0,0)):
        return mousePos.x > self.position.x and mousePos.x<self.position.x+self.dimensions.x
        

path = "Assets/"
textures = [
    #pygame.image.load("skybox.png"),
    pygame.image.load(path+"sky.png"), #since 0 is air in the raycasting algorithm, this address can be used for blank or testing pictures.
    pygame.image.load(path+"stone.png"),
    pygame.image.load(path+"stonebrick.png"),
]  
 
def drawMap():
    map = MAP_BUFFER
    row_size = int(math.sqrt(len(map)+1))   #grab some data needed for the for loop, including loading the map data
    x,y = 1,1
    for i in range(len(map)):
        if map[i] > 0:
            tile = pygame.transform.scale(textures[map[i]],(32,32))
            pygame.Surface.blit(win,tile,(x*32-32, y*32-32))
        x += 1                          #keeps track of the x and y coordinates of the tile by incrementing x for a row, then increment y and set x back to 0
        if x > row_size or y < 0: x = 1; y += 1 

def GUI():
    pygame.draw.rect(win, (250,250,250),(640,0,1280,640))
    
    for i in range(len(buttons)):
        buttons[i].blit()
    
def drawCursor():
    pygame.draw.rect(win,(255,165,0),(cursor_pos.y*32,cursor_pos.x*32,32,32),5)
    
def getInput():
    global cursor_pos, last_keyboard_pos
    mousePos = pygame.math.Vector2(pygame.mouse.get_pos())
    mapPos =pygame.math.Vector2(mousePos.y//32,mousePos.x//32)
    keys = pygame.key.get_pressed()
    if mousePos.x > 640:
        cursor_pos = last_keyboard_pos
        #move cursor
        if keys[K_a] and cursor_pos.y > 0:
            cursor_pos.y -= 1
        if keys[K_d] and cursor_pos.y <19:
            cursor_pos.y += 1
        if keys[K_w] and cursor_pos.x > 0:
            cursor_pos.x -= 1
        if keys[K_s] and cursor_pos.x <19:
            cursor_pos.x += 1
    #edit tiles
    else:
        last_keyboard_pos = cursor_pos
        cursor_pos = mapPos
    if pygame.mouse.get_pressed(3)[0]:
        MAP_BUFFER[int(20 * cursor_pos.x + cursor_pos.y)] = 1
    if pygame.mouse.get_pressed(3)[2]:
        MAP_BUFFER[int(20 * cursor_pos.x + cursor_pos.y)] = 0
    if keys[K_1]:
        MAP_BUFFER[int(20 * cursor_pos.x + cursor_pos.y)] = 1
    
MAP_BUFFER = readMapData("Map1.txt")
gui_start = 640
offset = 11
spacing = 64 + 22

buttons = [
    button((gui_start+offset        ,10),"stonebrick.png"),
    button((gui_start+offset+spacing,10),"stone.png")
]
selected = buttons[0] #auxillary variable denoting which button is selected

file = input("Please Enter the Map you wish to Edit (Do not include the .txt)")
file = "Maps/"+file+".txt"
print("Opening Map...")
MAP_BUFFER = readMapData(file)
print("Map Opened Successfully")
print("Press Escape to Save Changes")

editing = True
while editing:
    drawMap()
    GUI()
    drawCursor()
    getInput()
    for event in pygame.event.get():
        if event.type == QUIT:
            editing = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                editing = False  
    pygame.display.update()
    clock.tick(60)
    win.fill((0,0,0))
    
print("Saving Map to file ",file)
writeMapData(MAP_BUFFER,file)