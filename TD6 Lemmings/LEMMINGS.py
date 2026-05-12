import pygame
import numpy as np
import os, inspect

# Chemin assets
scriptDIR = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))
assets = os.path.join(scriptDIR, "data")

# Chargement des png / sprites
fond = pygame.image.load(os.path.join(assets, "map.png"))
planche = pygame.image.load(os.path.join(assets, "planche.png"))
planche.set_colorkey((0,0,0))
sortie_img = pygame.image.load(os.path.join(assets, "sortie.png"))
sortie_img.set_colorkey((0,0,0))

# Découpe la planche de sprites par ligne
def get_sprites(row_id):
    sprites = []
    if (row_id + 1) * 30 > planche.get_height(): return []
    for i in range(18):
        s = planche.subsurface((30 * i, 30 * row_id, 30, 30))
        if s.get_at((10, 10)) != (255, 0, 0, 255):
            sprites.append(s)
    return sprites

# Initialisation pygame
pygame.init()
screen = pygame.display.set_mode([800, 400])
pygame.display.set_caption("TP Lemmings - ESIEE")
font = pygame.font.SysFont("Arial", 18, bold=True)
clock = pygame.time.Clock()

# États de la machine à états finis
MARCHE, CHUTE, STOP, MORT, CREUSE, SORTIE = 100, 200, 300, 400, 500, 600
BASH, MINE, BUILD, FLOAT, BOMB = 700, 800, 900, 1000, 1100
CLIMBER_TOOL, NUKE_TOOL = 1200, 1300
CLIMB = 1400

anim = {
    MARCHE: get_sprites(0),
    CHUTE:  get_sprites(1),
    CLIMB:  get_sprites(2),
    FLOAT:  get_sprites(3),
    STOP:   get_sprites(4),
    MORT:   get_sprites(5),
    BUILD:  get_sprites(6),
    CREUSE: get_sprites(7),
    MINE:   get_sprites(8),
    BASH:   get_sprites(9),
    BOMB:   get_sprites(10),
    SORTIE: get_sprites(0),
}

lemmings = []
compteur_spawn = 0
sauves = 0
morts = 0
outil_actif = None
termine = False

# Limite entre le terrain jouable et la barre de boutons
BUTTON_Y = 338
# On empêche les creusages de modifier les pixels sous la barre de boutons
fond.set_clip(pygame.Rect(0, 0, 800, BUTTON_Y))

# Vérifie si un pixel du fond est solide donc pas noir
# Tout < BUTTON_Y est indestructible
def is_solid(px, py):
    if 0 <= px < 800 and 0 <= py < BUTTON_Y:
        c = fond.get_at((int(px), int(py)))
        return (c[0] + c[1] + c[2]) > 0
    # En dehors du terrain plancher invisible en bas, vide ailleurs
    return 0 <= px < 800 and py >= BUTTON_Y

# Ordre des compétences
tools = [
    (STOP,         192), 
    (MINE,         240),  
    (CLIMBER_TOOL, 288),  
    (FLOAT,        336), 
    (BOMB,         384),  
    (BUILD,        432),  
    (CREUSE,       480),  
    (BASH,         528),  
    (NUKE_TOOL,    576), 
]

# Boucle de jeu principale
while not termine:
    ticks = pygame.time.get_ticks()
    t_idx = ticks // 100  # change toutes les 100ms

    # Rendu du fond et de la sortie
    screen.fill((20, 20, 20))
    screen.blit(fond, (0, 0))
    screen.blit(sortie_img, (710, 275))

    # Cadre blanc autour du bouton actif
    for st, x_pos in tools:
        if outil_actif == st:
            pygame.draw.rect(screen, (255, 255, 255), (x_pos, BUTTON_Y, 48, 62), 3)

    # Spawn des lemings
    if compteur_spawn < 15 and (t_idx + compteur_spawn * 15) % 25 == 0:
        if not any(l['y'] < 120 and abs(l['x'] - 250) < 20 for l in lemmings):
            compteur_spawn += 1
            lemmings.append({
                'x': 250, 'y': 100, 'vx': -2, 'etat': CHUTE,
                'drop': 0, 'id': np.random.randint(100), 'live': True,
                'parach': False, 'dig_tmr': 0, 'climber': False
            })

    # Gestion des clics 
    for e in pygame.event.get():
        if e.type == pygame.QUIT: termine = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            if BUTTON_Y <= p[1] <= 399:  # clic sur la barre de boutons
                for st, x_pos in tools:
                    if x_pos <= p[0] < x_pos + 48:
                        if st == NUKE_TOOL:
                            for nl in lemmings:
                                if nl['live'] and nl['etat'] not in [MORT, SORTIE, BOMB]:
                                    nl['etat'] = BOMB; nl['tmr'] = 60
                        else:
                            outil_actif = st if outil_actif != st else None
                        break
            elif p[1] < BUTTON_Y:  # clic sur un lemming dans le terrain
                for l in lemmings:
                    if abs(l['x'] + 15 - p[0]) < 25 and abs(l['y'] + 15 - p[1]) < 25:
                        if outil_actif == CLIMBER_TOOL:
                            l['climber'] = True
                        elif outil_actif == FLOAT:
                            l['parach'] = True
                        elif l['etat'] == MARCHE:
                            if outil_actif == STOP:
                                l['etat'], l['vx'] = STOP, 0
                            elif outil_actif in [CREUSE, BASH, MINE]:
                                l['etat'] = outil_actif
                                if outil_actif == CREUSE: l['dig_tmr'] = ticks
                            elif outil_actif == BUILD:
                                l['etat'], l['cnt'] = BUILD, 0
                            elif outil_actif == BOMB:
                                l['etat'], l['tmr'] = BOMB, 60
                        break

    #Transitions d'états
    for l in lemmings:
        if not l['live']: continue
        x, y = l['x'], l['y']

        if l['etat'] in [CHUTE, FLOAT]:
            if is_solid(x + 15, y + 30):  # touche le sol
                # Mort si chute trop longue sans parachute
                l['etat'] = MORT if (l['drop'] > 250 and not l['parach']) else MARCHE
                l['drop'] = 0
            elif l['parach']:
                l['etat'] = FLOAT

        elif l['etat'] == MARCHE:
            if abs(x + 15 - 735) < 15 and abs(y + 25 - 315) < 15:
                l['etat'] = SORTIE; continue

            # Montée d'une marche : si obstacle bas mais pas haut, on monte
            if is_solid(x + 15 + l['vx'] * 4, y + 25):
                if not is_solid(x + 15 + l['vx'] * 4, y + 10):
                    l['y'] -= 4
                else:  # mur trop haut : grimpe ou fait demi-tour
                    if l.get('climber', False): l['etat'] = CLIMB
                    else: l['vx'] *= -1

            if not is_solid(x + 15, y + 30):
                l['etat'] = CHUTE
            else:  # demi-tour si on rencontre un bloqueur
                for o in lemmings:
                    if o != l and o['etat'] == STOP and abs(o['x'] - l['x']) < 15 and abs(o['y'] - l['y']) < 10:
                        l['vx'] *= -1; break

        elif l['etat'] == CREUSE:
            if l['y'] + 35 >= BUTTON_Y:  #  bas du terrain
                l['etat'] = MARCHE
            elif not any(is_solid(x + 15, y + dy) for dy in range(35, 60, 5)):
                l['etat'] = CHUTE

        elif l['etat'] == BASH:
            if not any(is_solid(x + 15 + l['vx'] * 22, y + dy) for dy in range(5, 30, 5)):
                l['etat'] = MARCHE

        elif l['etat'] == MINE:
            if l['y'] + 30 >= BUTTON_Y or not any(is_solid(x + 15 + l['vx'] * 12, y + dy) for dy in range(25, 45, 5)):
                l['etat'] = MARCHE

        elif l['etat'] == BUILD:
            if l['cnt'] > 12 or is_solid(x + 15 + l['vx'] * 12, y + 10):
                l['etat'] = MARCHE

        elif l['etat'] == CLIMB:
            wall_x = x + 15 + (14 if l['vx'] > 0 else -14)
            if is_solid(x + 15, y):             # plafond => retombe de l'autre côté
                l['etat'] = CHUTE; l['vx'] *= -1
            elif not is_solid(wall_x, y + 15):  # plus de mur => sommet atteint, reprend la marche
                l['etat'] = MARCHE

    # Actions physiques, déplacements et modifications du décor
    for l in lemmings:
        if not l['live']: continue

        if l['etat'] == CHUTE:
            l['y'] += 4; l['drop'] += 4
        elif l['etat'] == FLOAT:
            l['y'] += 1; l['drop'] = 0
        elif l['etat'] == CLIMB:
            l['y'] -= 3
        elif l['etat'] == MARCHE:
            l['x'] += l['vx']
        elif l['etat'] == CREUSE:
            # Coup de pioche toutes les 2 secondes
            if ticks - l['dig_tmr'] >= 2000:
                pygame.draw.circle(fond, (0, 0, 0, 255), (int(l['x'] + 15), int(l['y'] + 35)), 18)
                l['y'] += 20; l['dig_tmr'] = ticks
        elif l['etat'] == BASH:
            pygame.draw.rect(fond, (0, 0, 0, 255), (int(l['x'] + 15 + (5 if l['vx'] > 0 else -30)), l['y'] + 2, 25, 28))
            l['x'] += l['vx'] * 1.5
        elif l['etat'] == MINE:
            pygame.draw.circle(fond, (0, 0, 0, 255), (int(l['x'] + 15 + (5 if l['vx'] > 0 else -25)), int(l['y'] + 35)), 18)
            l['x'] += l['vx'] * 1.2; l['y'] += 1
        elif l['etat'] == BUILD:
            if (ticks // 200) % 2 == 0:
                pygame.draw.rect(fond, (139, 69, 19, 255), (int(l['x'] + 15 + l['vx'] * 8), l['y'] + 28, 15, 5))
                l['x'] += l['vx'] * 3; l['y'] -= 3; l['cnt'] += 1
        elif l['etat'] == BOMB:
            l['tmr'] -= 0.5
            if l['tmr'] <= 0:
                pygame.draw.circle(fond, (0, 0, 0, 255), (int(l['x'] + 15), int(l['y'] + 15)), 40)
                l['live'] = False; morts += 1

    # Rendu des sprites 
    screen.set_clip(pygame.Rect(0, 0, 800, BUTTON_Y))
    lemmings_a_garder = []
    for l in lemmings:
        if not l['live']: continue
        s_list = anim[l['etat']]
        if s_list:
            s = s_list[(t_idx + l['id']) % len(s_list)]
            if l.get('vx', 0) > 0: s = pygame.transform.flip(s, True, False)
            screen.blit(s, (l['x'], l['y']))

                    # Attend la fin de l'animation avant de retirer le lemming
            if l['etat'] in [MORT, SORTIE] and (t_idx + l['id']) % len(s_list) == len(s_list) - 1:
                l['live'] = False
                if l['etat'] == SORTIE: sauves += 1
                else: morts += 1
                continue
        lemmings_a_garder.append(l)
    lemmings = lemmings_a_garder
    screen.set_clip(None)

    # Fin
    if sauves + morts == 15 and not lemmings:
        m = "VICTOIRE !" if sauves >= 10 else "RATE..."
        screen.blit(font.render(m, True, (0, 0, 255)), (350, 200))

    clock.tick(25)
    pygame.display.flip()

pygame.quit()