import pygame,sys; from pygame.locals import QUIT,KEYDOWN,K_ESCAPE
pygame.init()

font = pygame.font.Font("Assets/Pixeltype.ttf",30, bold=False, italic=False)

window = pygame.display.set_mode((1,1)) #size will get set later

textData = [
    [font.render("File 1",100,(0,0,0),('gray')),100,50],
    [font.render("File 2",100,(0,0,0),('gray')),200,50],
    [font.render("File 3",100,(0,0,0),('gray')),300,50], #this is a list of tuples, the tuples have 3 values each, a pygame
    [font.render("File 4",100,(0,0,0),('gray')),100,150],#surface object with rendered text, an x position, and a y position
    [font.render("File 5",100,(0,0,0),('gray')),200,150],#its faster (but more memory intensive) this way than just rendering
    [font.render("File 6",100,(0,0,0),('gray')),300,150,],#every frame because the text is only rendered once using this method.
]

def printText(data):
    pygame.Surface.blit(window,data[0],(data[1],data[2])) #takes the tuples from the textData[] list and will blit the tuple surface
                                                          #coordinates also stored in the tuple

def fileSelectMenu():
    isFinished = True
    window = pygame.display.set_mode((400+pygame.Surface.get_width(textData[0][0]),200+pygame.Surface.get_height(textData[0][0]))) #set the window to be 400,200, but add on more resolution based on the dimensions of the text on screen, the text is now centered on the screen
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
            printText(textData[x])
        print(pygame.Surface.get_width(textData[0][0]))
        print(pygame.Surface.get_height(textData[0][0]))
        
        