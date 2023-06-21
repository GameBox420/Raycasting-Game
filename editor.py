import pygame, sys,math
from pygame.locals import *
pygame.init()

win = pygame.display.set_mode((940,600))
cursor_pos = pygame.math.Vector2(0,0)
selected_pos = pygame.math.Vector2(0,0)
last_keyboard_pos = cursor_pos
clock = pygame.time.Clock()
MAP_BUFFER = [] #the map data
DRAW_BUFFER = 1 #the tile ID currently being drawn
file = str()

font = pygame.font.Font("Assets/Pixeltype.ttf",30, bold=False, italic=False)
textData = [
    [font.render("File 1",100,(0,0,0),('gray')),100,50],
    [font.render("File 2",100,(0,0,0),('gray')),200,50],
    [font.render("File 3",100,(0,0,0),('gray')),300,50], #this is a list of tuples, the tuples have 3 values each, a pygame
    [font.render("File 4",100,(0,0,0),('gray')),100,150],#surface object with rendered text, an x position, and a y position
    [font.render("File 5",100,(0,0,0),('gray')),200,150],#its faster (but more memory intensive) this way than just rendering
    [font.render("File 6",100,(0,0,0),('gray')),300,150,],#every frame because the text is only rendered once using this method.
]

def printText(data):
    pygame.Surface.blit(win,data[0],(data[1],data[2])) #takes the tuples from the textData[] list and will blit the tuple surface
                                                          #coordinates also stored in the tuple

def getCollision(textPosition, textDimensions, mousePos):
    #simple point to rectangle collision, check to see if point is in between the corners of the rect, if it is, they are colliding
    return (mousePos.x > textPosition.x and mousePos.x < textPosition.x + textDimensions.x) and (mousePos.y > textPosition.y and mousePos.y < textPosition.y+textDimensions.y)

def fileSelectMenu():
    isFinished = False #set window
    window = pygame.display.set_mode((400+pygame.Surface.get_width(textData[0][0]),200+pygame.Surface.get_height(textData[0][0]))) #set the window to be 400,200, but add on more resolution based on the dimensions of the text on screen, the text is now centered on the screen
    pygame.mouse.set_visible(True)
    while isFinished == False:
        pygame.display.update()
        window.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()            
        
        for x in range(len(textData)):
            printText(textData[x])          #for all the buttons in the text data array, draw them.
        for x in range(len(textData)):  
            if getCollision(pygame.math.Vector2(textData[x][1],textData[x][2]),
                            pygame.math.Vector2(pygame.Surface.get_width(textData[x][0]),pygame.Surface.get_height(textData[x][0])), #run the getCollision() function using data from
                            pygame.math.Vector2(pygame.mouse.get_pos())) and pygame.mouse.get_pressed(3)[0]:                         #the textData[] 
                #print("Mouse is coliding with button ",x)
                if pygame.mouse.get_pressed(3)[0]:              # if the mouse is in the button area and the mouse is clicked, then end the loop and return the file that needs to be loaded
                    #print("Clicked!")
                    pygame.mouse.set_visible(False)
                    isFinished = True
                    return str(x) + ".txt"

def writeMapData(map, file_name):
    file = open(file_name, "w")     #open the file to write, this also wipes any text on the file
    data = str()                    
    for i in range(len(map)):       #for each of the indexes in the array map,
        data += str(map[i])         #add it to the data string
    file.write(data)                #write the entire string to the file
        
def readMapData(file_name):
    file = open(file_name, "r")    #open the file to read
    data = file.read()             #saves all the text in the file as a string
    chars= len(data)               #the number of characters in data string
    array = []               
    for i in range(0,chars):                #for each character in the data string
        array.append(int(float(data[i])))   #append it to a list
    return array    #return the completed list

class button:
    def __init__(self,pos,texture):
        self.dimensions = pygame.math.Vector2(64,64)                    #each button is 64p x 64p
        self.surface = pygame.Surface(self.dimensions)                  #create surface object
        self.position = pygame.math.Vector2(pos)                        #position of the button
        self.file = pygame.image.load("Assets/"+texture)                
        self.aux = pygame.transform.scale(self.file,self.dimensions)    #strech the texture of the button over the button surface
        self.name = texture #name of the button
    def blit(self):
        pygame.Surface.blit(win,self.aux,(self.position))
    def getPressed(self, mousePos = pygame.math.Vector2(0,0)):
        #simple point to rectangle collision, check to see if point is in between the corners of the rect, if it is, they are colliding
        return mousePos.x > self.position.x and mousePos.x<self.position.x+self.dimensions.x and mousePos.y > self.position.y and mousePos.y < self.position.y + self.dimensions.y and pygame.mouse.get_pressed(3)[0]
        
        

path = "Assets/"
textures = [
    pygame.image.load(path+"sky.png"), #since 0 is air in the raycasting algorithm, this address can be used for blank or testing pictures.
    pygame.image.load(path+"stone.png"),
    pygame.image.load(path+"stonebrick.png"),
    pygame.image.load(path+"dirt.png"),
    pygame.image.load(path+"wood.png"),                 #image.load() save the pictures as pygame surfaces
    pygame.image.load(path+"leaves.png"),
    pygame.image.load(path+"cloth.png"),
    pygame.image.load(path+"bluebrick.png")
] 
gui_start = 640
offset = 11
spacing = 64 + 22
DRAW_BUFFER = 0 #auxillary variable denoting which button is selected
buttons = [
    button((1000,1000),"sky.png"), #dummy button to make the indexes of textures[] and buttons[] corsespond to eachother
    button((gui_start+offset          ,10),"stone.png"),
    button((gui_start+offset+spacing  ,10),"stonebrick.png"),
    button((gui_start+offset+2*spacing,10),"dirt.png"),
    button((gui_start+offset          ,84),"wood.png"),         #im using the variables to determine the correct spacing of each button
    button((gui_start+offset+spacing  ,84),"leaves.png"),     
    button((gui_start+offset+2*spacing,84),"cloth.png"),
    button((gui_start+offset          ,158),"bluebrick.png")
]
 
def drawMap():
    row_size = int(math.sqrt(len(MAP_BUFFER)+1))   #grab some data needed for the for loop, including loading the map data
    x,y,i = 1,1,0
    for i in range(len(MAP_BUFFER)):
        if MAP_BUFFER[i] > 0:
            tile = pygame.transform.scale(textures[MAP_BUFFER[i]],(32,32))
            pygame.Surface.blit(win,tile,(x*32-32, y*32-32))
        x += 1                          #keeps track of the x and y coordinates of the tile by incrementing x for a row, then increment y and set x back to 0
        if x > row_size or y < 0: x = 1; y += 1

def GUI():
    global selected_pos, DRAW_BUFFER
    pygame.draw.rect(win, (250,250,250),(640,0,1280,640))
    #draw buttons and check for clicks
    for i in range(len(buttons)):
        buttons[i].blit()
        if buttons[i].getPressed(pygame.math.Vector2(pygame.mouse.get_pos())):
            DRAW_BUFFER = i
            selected_pos = buttons[i].position
    pygame.draw.rect(win, (250,165,0),(selected_pos.x,selected_pos.y,64,64),2)
        
    
def drawCursor():
    pygame.draw.rect(win,(255,165,0),(cursor_pos.y*32,cursor_pos.x*32,32,32),5)
    
def getInput():
    global cursor_pos, last_keyboard_pos
    mousePos = pygame.math.Vector2(pygame.mouse.get_pos())
    mapPos =pygame.math.Vector2(mousePos.y//32,mousePos.x//32)
    keys = pygame.key.get_pressed()
    #move cursor, if mouse is on the map grid, use mouse position, if it isnt, use WASD to move cursor
    if mousePos.x > 640:
        cursor_pos = last_keyboard_pos
    #edit tiles
    else:
        last_keyboard_pos = cursor_pos
        cursor_pos = mapPos
        if pygame.mouse.get_pressed(3)[0]:
            print("Drew ID ",DRAW_BUFFER," at coordinate ",cursor_pos)
            MAP_BUFFER[int(20 * cursor_pos.x + cursor_pos.y)] = DRAW_BUFFER
        if pygame.mouse.get_pressed(3)[2]:
            MAP_BUFFER[int(20 * cursor_pos.x + cursor_pos.y)] = 0
        if keys[K_1]:
            MAP_BUFFER[int(20 * cursor_pos.x + cursor_pos.y)] = 1
    

selected_pos = buttons[0].position

def printMapData(file_name):
    file = open(file_name, 'r')
    data = file.read()
    print(data)
    


def runEditor():
    global MAP_BUFFER, DRAW_BUFFER
    pygame.mouse.set_visible(True)
    file = fileSelectMenu()
    MAP_BUFFER = readMapData(file)

    pygame.mouse.set_visible(True)
    win = pygame.display.set_mode((940,650))
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
    pygame.mouse.set_visible(True)
