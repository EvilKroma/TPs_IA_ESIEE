import pygame
import numpy as np
import pygame.surfarray as surfarray
import math

# --- CONFIGURATION & PALETTE ---
palette = {} 
palette['B'] = [0, 0, 255]      # Mur (Blue)
palette[' '] = [0, 0, 0]        # Sol (Black)
palette['W'] = [255, 255, 255]  # Blanc (Eclat)
palette['R'] = [255, 0, 0]      # Piège (Red)
palette['Y'] = [255, 255, 0]    # Sortie (Yellow)
palette['O'] = [255, 165, 0]    # Or / Coffre (Orange)
palette['K'] = [218, 165, 32]   # Clé (Gold)
palette['D'] = [139, 69, 19]    # Porte (Brown)
palette['G'] = [0, 255, 0]      # Vert (Sac à dos)
palette['C'] = [0, 225, 255]    # Cyan (Jambes)

WIDTH = 40  
NBcases = 20

# --- PLAN DU LABYRINTHE ---
plan = [ 
    'BBBBBBBBBBBBBBBBBBBB', 
    'B                  B',
    'B BBB B BBBBBB BBB B',
    'B B   B B    B B   B',
    'B B BBB B BB B B BBB',
    'B B     B B  B B   B',
    'B BBBBBBB B BB BBB B',
    'B       B B      B B',
    'BBBBB B B BBBBBB B B',
    'B     B B B    B B B',
    'B BBBBB B B BB B B B',
    'B B     B    B   B B',
    'B B BBBBBBBBBB BBB B',
    'B B B          B   B',
    'B B B BBBBBBBBBB B B',
    'B   B B          B B',
    'BBBBB B BBBBBBBBBB B',
    'B     B            B',
    'B BBBBBBBBBBBBBBBB B',
    'BBBBBBBBBBBBBBBBBBBB' 
]

LABY = np.zeros((NBcases,NBcases,3), dtype=np.uint8)
for y in range(NBcases):
    ligne = plan[y]
    for x in range(NBcases):
        LABY[x,y] = palette[ligne[x]]
        
def ToSprite(ascii):
   _larg = len(max(ascii, key=len))
   _haut = len(ascii)
   TBL = np.zeros((_larg,_haut,3), dtype=np.uint8)
   for y in range(_haut):
      ligne = ascii[y]
      for x in range(len(ligne)):
         if ligne[x] in palette: TBL[x,y] = palette[ligne[x]]
   return surfarray.make_surface(TBL)

# --- SPRITES AMELIORES ---
# Personnage avec jambes visibles (11 lignes de haut)
pers1 = [ '  RRR   ', ' RRWWR  ', '  RRR   ', '  YY    ', '  YYY   ', '  YY YG ', '  GG    ', '  CC    ', '  CC    ', ' C  C   ', ' C  C   ' ]
pers2 = [ '  RRR   ', ' RRWWR  ', '  RRR   ', '  YY    ', '  YYY   ', '  YY YG ', '  GG    ', '  CC    ', '  CC    ', '  CC    ', '  CC    ' ]
pers3 = [ '  RRR   ', ' RRWWR  ', '  RRR   ', '  YY    ', '  YYY   ', '  YY YG ', '  GG    ', '  CC    ', '  CC    ', '   C  C ', '   C  C ' ]

# Piège : Piques (Spikes)
sprite_trap = ToSprite([
    'R   R',
    ' R R ',
    'R R R',
    ' R R ',
    'R R R'
])

# Trésor : Coffre brillant
sprite_gold = ToSprite([
    ' OOO ',
    'OOWOO',
    'OOOOO',
    'DODOD',
    'DDDDD'
])

# Clé, Porte, Sortie
sprite_key   = ToSprite([ ' KKK ', ' K K ', ' KKK ', '  K  ', ' KKK ', '  K  ' ])
sprite_key_inv = pygame.transform.scale(sprite_key, (15, 22))
sprite_door  = ToSprite([ 'DDDDD', 'D D D', 'DDDDD', 'D D D', 'DDDDD' ])
sprite_exit  = ToSprite([ 'YYYYY', 'Y   Y', 'Y   Y', 'Y   Y', 'YYYYY' ])

player_sprites = [ToSprite(pers1), ToSprite(pers2), ToSprite(pers3), ToSprite(pers2)]
player_x, player_y = 50, 50 
player_speed = 4

def get_pos(gx, gy): return (gx * WIDTH + 10, gy * WIDTH + 10)

exit_pos = get_pos(18, 1)
door_pos = get_pos(17, 1)
key_pos  = get_pos(1, 17)
traps = [get_pos(7, 3), get_pos(13, 5), get_pos(1, 11), get_pos(11, 11), get_pos(18, 17)]
golds = [get_pos(10, 1), get_pos(3, 7), get_pos(15, 7), get_pos(11, 13)]

has_key = False
game_won = False
score = 0
pygame.init()
screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("GAUNTLET - TD4")
font = pygame.font.SysFont("Arial", 26)
font_big = pygame.font.SysFont("Arial", 90, bold=True)
clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
            
    KeysPressed = pygame.key.get_pressed()
    dx, dy, moving = 0, 0, False
    
    if not game_won:
        if KeysPressed[pygame.K_UP]:    dy -= player_speed
        if KeysPressed[pygame.K_DOWN]:  dy += player_speed
        if KeysPressed[pygame.K_LEFT]:  dx -= player_speed
        if KeysPressed[pygame.K_RIGHT]: dx += player_speed
    
    # 1. Dessin LABY
    for ix in range(NBcases):
        for iy in range(NBcases):
            pygame.draw.rect(screen, LABY[ix,iy], [WIDTH * ix, WIDTH * iy, WIDTH, WIDTH])
    
    # 2. Collisions Murs (Corps réduit pour la souplesse)
    pw, ph = player_sprites[0].get_size()
    if 0 <= player_x + dx < 800:
        if screen.get_at((int(player_x + dx + (pw//2 if dx>0 else 0)), int(player_y + ph//2)))[2] != 255:
            player_x += dx
            if dx != 0: moving = True
    if 0 <= player_y + dy < 800:
        if screen.get_at((int(player_x + pw//2), int(player_y + dy + (ph//2 if dy>0 else 0))))[2] != 255:
            player_y += dy
            if dy != 0: moving = True

    # 3. Animation des Jambes (Utilisation du modulo selon l'indice)
    # On change de frame toutes les 250ms (ticks/250)
    if moving:
        anim_idx = (pygame.time.get_ticks() // 250) % len(player_sprites)
    else:
        anim_idx = 1 # Sprite statique (jambes serrées)
    
    # 4. Logique Objets
    if not game_won:
        for g in golds[:]:
            if math.hypot(player_x-g[0], player_y-g[1]) < 18:
                golds.remove(g); score += 100
        for t in traps:
            if math.hypot(player_x-t[0], player_y-t[1]) < 10: # Distance collision piège
                player_x, player_y = 50, 50 
        if not has_key and math.hypot(player_x-key_pos[0], player_y-key_pos[1]) < 18:
            has_key = True
        if has_key and math.hypot(player_x-exit_pos[0], player_y-exit_pos[1]) < 15:
            game_won = True

    # 5. Affichage
    for g in golds: screen.blit(sprite_gold, g)
    for t in traps: screen.blit(sprite_trap, t)
    if not has_key: screen.blit(sprite_key, key_pos)
    screen.blit(sprite_door, door_pos)
    screen.blit(sprite_exit, exit_pos)
    screen.blit(player_sprites[anim_idx], (player_x, player_y))
    
    # UI
    screen.blit(font.render(f"SCORE: {score}", True, (255,255,255)), (20, 10))
    if has_key:
        screen.blit(font.render("INVENTAIRE:", True, (255,255,255)), (180, 10))
        screen.blit(sprite_key_inv, (350, 12))
    elif math.hypot(player_x-door_pos[0], player_y-door_pos[1]) < 60:
        screen.blit(font.render("CHERCHE LA CLE !", True, (255,100,100)), (250, 10))

    if game_won:
        s = pygame.Surface((800,800), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        screen.blit(s, (0,0))
        screen.blit(font_big.render("VICTOIRE !", True, (0,255,0)), (180, 350))

    pygame.display.flip()
    clock.tick(30)
pygame.quit()
