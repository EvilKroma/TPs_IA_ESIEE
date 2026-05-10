# permet d'accéder aux fonctions du module pygame
import pygame

# Definit des couleurs RGB
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BLUE = [0 , 0 , 255]

# initialisation de l'écran de jeu
pygame.init()

# Initialise la fenêtre de jeu
TailleEcran = [400, 300]
screen = pygame.display.set_mode(TailleEcran)
pygame.display.set_caption("Super Ball")

# Gestion du rafraichissement de l'écran
clock = pygame.time.Clock()

# Position de départ
balle_x = 50
balle_y = 50

# Vitesse et direction
balle_change_x = 3
balle_change_y = 3

balle_rayon= 5

# Le jeu continue tant que l'utilisateur ne ferme pas la fenêtre
Termine = False

# BOUCLE PRINCIPALE DU PROGRAMME
while not Termine:
  # recupère la liste des évènements du joueur
  event = pygame.event.Event(pygame.USEREVENT)

  # EVENEMENTS
  # détecte le clic sur le bouton close de la fenêtre
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      Termine = True

  # LOGIQUE
  # Déplace la balle
  balle_x += balle_change_x
  balle_y += balle_change_y

  # Rebond
  if balle_y > TailleEcran[1] or balle_y < 0:
    balle_change_y = balle_change_y * -1
  if balle_x > TailleEcran[0] or balle_x < 0:
    balle_change_x = balle_change_x * -1

  # AFFICHAGE
  # Dessine le fond
  screen.fill(WHITE)

  # Colorie les bords de l'écran
  R = [0,0, TailleEcran[0],  TailleEcran[1]]
  pygame.draw.rect(screen,GREEN,R ,1)


  # dessine le palet de jeu
  pygame.draw.circle(screen,RED,[balle_x,balle_y],balle_rayon *2)
  pygame.draw.circle(screen,BLACK,[balle_x,balle_y],balle_rayon )

  # Demande à pygame de se caler sur 30 FPS
  clock.tick(30)

  # Bascule l'image dessinée à l'écran
  pygame.display.flip()

  #debug
  print("position : " + str([balle_x,balle_y]))
  print("Dir : " + str([balle_change_x,balle_change_y]))

# Ferme la fenêtre
pygame.quit()
