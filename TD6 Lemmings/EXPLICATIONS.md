# TD Lemmings

Ce projet est une implémentation simplifiée du jeu Lemmings utilisant Pygame. L'objectif est de gérer une intelligence artificielle via une machine à états finis.

## Architecture du code

### 1. La machine à états (FSM)
Chaque lemming possède un état (`etat`) qui définit son comportement.  
* **Mouvements de base** : marche et chute.
* **Capacités spéciales** : stop (bloqueur), creuse (vertical), bash (horizontal), mine (diagonal), build (escaliers), float (parachute) et bomb (explosion).
* **Fin de cycle** : mort ou sortie.

### 2. Gestion des collisions (la méthode du pixel)
Au lieu d'utiliser des masques de collision complexes, le code utilise la fonction `is_solid(x, y)`.
* Elle vérifie la couleur du pixel sur l'image `fond`.
* Si le pixel est **noir**, c'est du vide.
* Si le pixel a une **couleur**, c'est un obstacle solide.

### 3. Terrain destructible
C'est le point fort du projet. Pour "détruire" le décor :
* On dessine directement des formes noires (`pygame.draw.circle` ou `rect`) sur la surface `fond`.
* Comme `is_solid` ne détecte que les pixels non noirs, le décor devient instantanément traversable là où on a dessiné.

### 4. Logique de montée (step-up)
Pour que les lemmings montent les escaliers sans se retourner :
* On teste s'il y a un obstacle au niveau des pieds.
* Si oui, on teste s'il y a du vide au niveau de la tête.
* Si le passage est libre en haut, on téléporte le lemming de quelques pixels vers le haut pour simuler la montée d'une marche.

## Comment l'expliquer à l'oral ?
1. **Le spawn** : "Les lemmings sont créés dans une liste et tombent par défaut."
2. **L'IA** : "Chaque lemming analyse son environnement à chaque frame (pixel sous ses pieds, pixel devant lui) pour décider s'il doit changer d'état."
3. **L'interface** : "On détecte le clic sur la zone basse pour changer l'outil actif, puis le clic sur un lemming pour modifier son dictionnaire d'état."
4. **L'animation** : "On utilise le temps global de Pygame pour calculer l'index de l'image à afficher, avec un décalage aléatoire pour que les lemmings ne soient pas tous synchronisés."
