import pygame, math
pygame.init()
#main game variables
vec = pygame.math.Vector2 #2 for two dimensional
RES_H = 1080
RES_W = 1920
FPS = 60
PI = math.pi;P2 = PI/2;P3 = 3*PI/2;DR = 0.0174533
gameClock = pygame.time.Clock()
win = pygame.display.set_mode((RES_W, RES_H),flags=pygame.FULLSCREEN,vsync=1)
pygame.mouse.set_visible(False)

#raycasting variables
mapx, mapy= 20, 20 #the length and width of the map in units
blockRes = 64 #the resolution of the
FOV = 60 #FOV in degrees.
NOR = int(RES_W/4) #the number of rays cast
Rays_Per_Radian = NOR/FOV #how many rays in 1 radian
inc = DR/Rays_Per_Radian #angle to increment the rays by each iteration
width = RES_W/NOR #width of each ray once its drawn on the screen
#horizon = RES_H/2 #initial y-position on the screen to draw from.
maxdof = 20
maxDistance = maxdof*blockRes #the farthest a ray can possibly be
blkDistance = 300 #the farthest a ray can be before it is drawn all black
isDaytime = True
path = "Assets/" #the path of all the pics nad fonts
#all of the images and font variables loaded from files
textures = [
    #pygame.image.load("skybox.png"),
    pygame.image.load(path+"sky.png"), #since 0 is air in the raycasting algorithm, this address can be used for blank or testing pictures.
    pygame.image.load(path+"stone.png"),
    pygame.image.load(path+"stonebrick.png"),
    pygame.image.load(path+"dirt.png"),
    pygame.image.load(path+"wood.png"),
    pygame.image.load(path+"leaves.png"),
    pygame.image.load(path+"cloth.png"),
    pygame.image.load(path+"bluebrick.png")
]
gameFont = pygame.font.Font(path+"Pixeltype.ttf",30)

pygame.mixer.music.load(path+"music.mp3")
pygame.mixer.music.play(-1)