import pygame
import os, inspect
from pygame.transform import scale

#recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"data")


# Setup
pygame.init()

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]

police = pygame.font.SysFont("arial", 15)
 
 
print(scriptDIR)
 
 
# Set the width and height of the screen [width,height]
screeenWidth = 800
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth,screenHeight))
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(True) 
 

fond = pygame.image.load(os.path.join(assets, "fond.bmp"))
# Chargement des images pour chaque poisson
poisson1_img = pygame.image.load(os.path.join(assets, "fish1.bmp")).convert()
color_key1 = poisson1_img.get_at((0, 0))
poisson1_img.set_colorkey(color_key1)

poisson2_img = pygame.image.load(os.path.join(assets, "fish2.bmp")).convert()
color_key2 = poisson2_img.get_at((0, 0))
poisson2_img.set_colorkey(color_key2)

# Variables pour savoir si les poissons sont retournés
poisson1_flipped = False
poisson2_flipped = False

plant1 = pygame.image.load(os.path.join(assets, "plant1.bmp"))
color_key3 = plant1.get_at((0, 0))
plant1.set_colorkey(color_key3)
plant1 = pygame.transform.scale(plant1, (300, 300))
 
 


poisson1_x  = 100
poisson1_y  = 200
poisson1_vx = -2

poisson2_x  = 200
poisson2_y  = 100
poisson2_vx = 4
 
 
# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
   # récupère la liste des touches claviers appuyeées sous la forme liste bool
   pygame.event.pump()
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
      
   
    # LOGIQUE
 

   # Poisson 1
   poisson1_x += poisson1_vx
   if ( poisson1_x < 50 ):
      poisson1_x = 50
      poisson1_vx = -poisson1_vx
      poisson1_flipped = not poisson1_flipped

   if ( poisson1_x > (3/4 * screeenWidth) ):
      poisson1_x = (3/4 * screeenWidth)
      poisson1_vx = -poisson1_vx
      poisson1_flipped = not poisson1_flipped

   # Poisson 2
   poisson2_x += poisson2_vx
   if ( poisson2_x < 50 ):
      poisson2_x = 50
      poisson2_vx = -poisson2_vx
      poisson2_flipped = not poisson2_flipped

   if ( poisson2_x > (3/4 * screeenWidth) ):
      poisson2_x = (3/4 * screeenWidth)
      poisson2_vx = -poisson2_vx
      poisson2_flipped = not poisson2_flipped


    # DESSIN
    
   # affiche la zone de rendu au dessus de fenetre de jeu

   screen.blit(fond,(0,0))


   # Affichage de la plante (en bas à gauche)
   plant1_rect = plant1.get_rect()
   plant1_x = 30
   plant1_y = screenHeight - plant1_rect.height
   screen.blit(plant1, (plant1_x, plant1_y))

   # Affichage du poisson 1
   img1 = pygame.transform.flip(poisson1_img, True, False) if poisson1_flipped else poisson1_img
   screen.blit(img1, (poisson1_x, poisson1_y))

   # Affichage du poisson 2
   img2 = pygame.transform.flip(poisson2_img, True, False) if poisson2_flipped else poisson2_img
   screen.blit(img2, (poisson2_x, poisson2_y))

   # Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(30)
 
# Close the window and quit.
pygame.quit()