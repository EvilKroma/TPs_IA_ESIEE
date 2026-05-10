# TD gauntlet

Ce document résume le fonctionnement technique du projet Gauntlet réalisé avec Pygame.

## 1. Structure de l'environnement
*   **Palette de couleurs (`palette`) :** Un dictionnaire associe des lettres (B, W, G, R...) à des codes couleur RGB.
*   **Plan du labyrinthe (`plan`) :** Le niveau est défini par une grille de 20x20 caractères (une liste de chaînes).
*   **Conversion en surface (`LABY`) :** Le plan est converti en un tableau Numpy de couleurs, puis dessiné à l'écran sous forme de rectangles de 40x40 pixels (`WIDTH`).

## 2. Système de sprites et animation
*   **Fonction `ToSprite(ascii)` :** Elle transforme des listes de chaînes de caractères (dessins en ASCII art) en surfaces Pygame utilisables comme images.
*   **Animation de marche :** Trois versions du personnage (`pers1`, `pers2`, `pers3`) sont alternées toutes les 150ms à l'aide de `pygame.time.get_ticks() % len(player_sprites)`. Cela crée un mouvement fluide des jambes.

## 3. Mécaniques de jeu
*   **Déplacements :** Le joueur se déplace de 4 pixels par tour (`player_speed`) si une touche fléchée est pressée.
*   **Gestion des collisions (murs) :** 
    *   Avant de valider un mouvement, le code teste la couleur du pixel à l'écran juste devant le personnage via `screen.get_at()`.
    *   Si le pixel est bleu (couleur des murs), la variable `can_move` passe à `False`, bloquant ainsi le personnage.
*   **Gestion des objets (trésors, pièges, clé) :** 
    *   On calcule la distance mathématique (Pythagore) entre le joueur et l'objet : $d = \sqrt{(x1-x2)^2 + (y1-y2)^2}$.
    *   Si cette distance est inférieure à un seuil (ex: 20-25 pixels), l'action se déclenche (gain de points, retour au départ ou ramassage de la clé).

## 4. Conditions de victoire
*   Le joueur doit d'abord posséder la clé (`has_key = True`).
*   Il doit ensuite s'approcher à moins de 15 pixels de la sortie (`exit_pos`).
*   Le message "WIN" s'affiche alors en gros au centre de l'écran.

## 5. Boucle principale
Le jeu tourne à 30 FPS (`clock.tick(30)`). À chaque itération :
1.  On efface et redessine le labyrinthe.
2.  On capture les entrées clavier.
3.  On calcule la physique (collisions et distances).
4.  On dessine les sprites et l'interface (score, inventaire).
5.  On rafraîchit l'affichage (`pygame.display.flip()`).

