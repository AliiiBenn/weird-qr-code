# Tâches : Module de Gestion de la Grille Hexagonale (Étape 1)

L'objectif de cette première étape est de développer les fondations pour manipuler et représenter une grille d'hexagones.

## 1. Conception et Initialisation de la Grille

-   [x] **Choisir l'orientation des hexagones :**
    -   [ ] Option 1 : "Pointy-top" (pointe en haut/bas)
    -   [x] Option 2 : "Flat-top" (côté plat en haut/bas) - **CHOISI**
    -   Documenter le choix et sa justification (si nécessaire).
-   [ ] **Définir le système de coordonnées hexagonales :**
    -   [ ] Implémenter les coordonnées axiales (`q`, `r`) comme système principal.
    -   [x] Considérer la relation avec les coordonnées cubiques (`x`, `y`, `z` avec `x+y+z=0`) pour certaines opérations si cela simplifie (ex: distances, rotations).
-   [x] **Définir le système de coordonnées hexagonales (pour positions absolues) :**
    -   [x] Définir une structure (ex: `dataclass AxialPos(q: int, r: int)`) pour les coordonnées axiales absolues (sans la restriction `Literal[-1,0,1]`).
-   [x] **Définir une structure pour les directions/déplacements axiaux unitaires :**
    -   [x] La classe `AxialCoordinates` actuelle (dans `src/core/hex_grid.py`) avec validation `Literal[-1,0,1]` sert ce rôle.
-   [x] Définir les 6 constantes de direction (ex: `HEX_DIRECTIONS_FLAT_TOP`) en utilisant `AxialCoordinates`.
-   [ ] **Définir les paramètres de base de l'hexagone :**
    -   [ ] Taille de l'hexagone (ex: rayon, distance du centre à un sommet, ou longueur d'un côté).
    -   [ ] Origine de la grille (position du pixel pour l'hexagone `(0,0)`).
-   [x] **Définir les paramètres de base de l'hexagone et le layout de la grille :**
    -   [x] Définir `PixelCoord(x: float, y: float)` pour les coordonnées en pixels. (Fait dans `src/core/hex_grid.py`)
    -   [x] Définir `HexgridLayout(size: float, origin: PixelCoord)` pour encapsuler la taille de l'hexagone (distance centre-sommet) et l'origine de la grille. (Fait dans `src/core/hex_grid.py`)

## 2. Fonctions de Conversion de Coordonnées

-   [x] **`hex_to_pixel(hex_q, hex_r)` :** (Implémentée comme méthode `HexgridLayout.hex_to_pixel(hex_pos: AxialPos)`)
    -   [x] Prend les coordonnées axiales (`q`, `r`) d'un hexagone.
    -   [x] Retourne les coordonnées cartésiennes (`pixel_x`, `pixel_y`) du centre de cet hexagone.
    -   [x] Doit prendre en compte l'orientation ("flat-top" implicite) et la taille de l'hexagone, ainsi que l'origine de la grille.
-   [ ] **`pixel_to_hex(pixel_x, pixel_y)` (Plus tard, utile pour le décodeur) :**
    -   Prend des coordonnées cartésiennes (`pixel_x`, `pixel_y`).
    -   Retourne les coordonnées axiales (`q`, `r`) de l'hexagone contenant ce pixel.
    -   Nécessite de gérer l'arrondi correct vers l'hexagone le plus proche.
-   [x] **`get_hexagon_vertices(hex_q, hex_r)` ou `get_hexagon_vertices(center_pixel_x, center_pixel_y)` :** (Implémentée comme méthode `HexgridLayout.get_hexagon_vertices(hex_pos: AxialPos)`)
    -   Prend soit les coordonnées d'un hexagone, soit le centre en pixels.
    -   Retourne une liste des 6 coordonnées cartésiennes (`pixel_x`, `pixel_y`) des sommets de cet hexagone.
    -   Utile pour le dessin.

## 3. Opérations sur la Grille Hexagonale

-   [ ] **`hex_neighbors(hex_q, hex_r)` :**
    -   Prend les coordonnées axiales (`q`, `r`) d'un hexagone.
    -   Retourne une liste des 6 coordonnées axiales de ses hexagones voisins.
-   [ ] **`hex_distance(hex_q1, hex_r1, hex_q2, hex_r2)` :**
    -   Calcule la distance (en nombre d'hexagones) entre deux hexagones donnés par leurs coordonnées axiales.

## 4. Structure du Code (Proposition)

-   [x] Créer un fichier `hex_grid.py` (ou nom similaire).
-   [ ] Envisager une classe `Hexagon` qui pourrait stocker ses coordonnées (`q`, `r`) et potentiellement offrir des méthodes (comme `to_pixel()`, `get_vertices()`, `get_neighbors()`).
-   [ ] Ou, utiliser des fonctions utilitaires si une approche purement fonctionnelle est préférée pour ce module.
-   [x] **Utiliser systématiquement les annotations de type Python (PEP 484, compatible Python 3.10+) pour toutes les signatures de fonctions, variables, et attributs de classe.**

## 5. Tests et Visualisation Initiale

-   [x] **Tests Unitaires :**
    -   [x] Pour la classe `AxialCoordinates` (actuellement servant de direction/déplacement unitaire) : valider instanciation, accès aux propriétés, `__str__`, et gestion des valeurs invalides (fait dans `tests/core/test_hex_grid.py`).
    -   [x] Pour `hex_to_pixel` et `pixel_to_hex` (si implémenté tôt) avec des valeurs connues. (`hex_to_pixel` testé via `TestHexgridLayout` ; `pixel_to_hex` est pour plus tard).
    -   [x] Pour `get_hexagon_vertices` avec des valeurs connues (testé via `TestHexgridLayout`).
    -   [x] Pour `hex_neighbors` (vérifier que les voisins d'un hexagone donné sont corrects).
    -   [x] Pour `hex_distance` avec des cas simples.
-   [ ] **Script de Visualisation :**
    -   [ ] Créer un petit script (utilisant Pillow par exemple) qui :
    -   [ ] Définit une petite grille (ex: 3x3 ou 5x5 hexagones).
    -   [ ] Utilise `hex_to_pixel` et `get_hexagon_vertices` pour dessiner ces hexagones.
    -   [ ] Permet de vérifier visuellement que les calculs de position et de forme sont corrects.
    -   [ ] Optionnel : afficher les coordonnées (`q`,`r`) au centre de chaque hexagone dessiné.
    -   [x] **Script de Visualisation :** (Implémenté dans `visualize_grid.py`)
        -   [x] Créer un petit script (utilisant Pillow par exemple) qui :
        -   [x] Définit une petite grille (ex: 3x3 ou 5x5 hexagones).
        -   [x] Utilise `hex_to_pixel` et `get_hexagon_vertices` pour dessiner ces hexagones.
        -   [x] Permet de vérifier visuellement que les calculs de position et de forme sont corrects.
        -   [x] Optionnel : afficher les coordonnées (`q`,`r`) au centre de chaque hexagone dessiné.

## Critères de Fin d'Étape

-   Toutes les fonctions de conversion de coordonnées et d'opérations de base sur la grille sont implémentées et testées.
-   Un script de visualisation simple permet de confirmer le bon fonctionnement de la géométrie hexagonale.
-   Le code est structuré de manière claire et réutilisable.

## 6. Utilitaires de Validation (Inspiré par les descripteurs Python)

-   [ ] **Créer le fichier `src/utils/validators.py` pour héberger ce code.**
-   [x] **Définir une classe abstraite `Validator(ABC)` :**
    -   [x] Importer `ABC` et `abstractmethod` depuis le module `abc`.
    -   [x] La classe `Validator` doit hériter de `ABC`.
    -   [x] Implémenter `__set_name__(self, owner: type, name: str) -> None`:
        -   Stocke `name` dans un attribut privé (ex: `self.private_name = '_' + name`).
    -   [x] Implémenter `__get__(self, obj: object, objtype: type | None = None) -> object`:
        -   Retourne `getattr(obj, self.private_name)`.
    -   [x] Implémenter `__set__(self, obj: object, value: object) -> None`:
        -   Appelle `self.validate(value)`.
        -   Appelle `setattr(obj, self.private_name, value)`.
    -   [x] Définir `@abstractmethod
    def validate(self, value: object) -> None:`
        -   `pass` (l'implémentation sera dans les sous-classes).
-   [ ] **Implémenter un validateur spécifique `OneOf(Validator)` :**
    -   [ ] `__init__(self, *options: object) -> None`:
        -   Stocke `set(options)` dans un attribut (ex: `self.options`).
    -   [ ] `validate(self, value: object) -> None`:
        -   Vérifie si `value not in self.options`.
        -   Si c'est le cas, lève une `ValueError` avec un message descriptif (ex: `f"La valeur {value!r} n'est pas l'une des options valides : {self.options!r}"`).
-   [x] **Utiliser systématiquement les annotations de type Python (PEP 484, compatible Python 3.10+) pour toutes les signatures et attributs des validateurs.** (Appliqué aux classes Validator et OneOf)
-   [x] **Implémenter un validateur spécifique `OneOf(Validator[T_Val])` :**
    -   [x] Hérite de `Validator[T_Val]` (où `T_Val` est le `TypeVar` défini précédemment).
    -   [x] `__init__(self, *options: T_Val) -> None`:
        -   Stocke `set(options)` dans un attribut (ex: `self.options: set[T_Val]`).
    -   [x] `validate(self, value: T_Val) -> None`:
        -   Vérifie si `value not in self.options`.
        -   Si c'est le cas, lève une `ValueError`