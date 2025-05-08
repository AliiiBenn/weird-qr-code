# Tâches : Implémentation des Repères d'Alignement (Finder Patterns)

L'objectif est d'implémenter le dessin des trois repères d'alignement spécifiés dans le plan de développement (section 1.2).

## 1. Prérequis et Configuration

-   [x] **Définir les constantes de couleur :**
    -   [x] Créer un fichier `src/core/constants.py`.
    -   [x] Définir une `Enum ProtocolColor(Enum)` avec `BLACK`, `RED`, `BLUE`, `WHITE` et une propriété `.rgb`.
    -   [x] Définir `FINDER_COLORS: dict[str, dict[str, ProtocolColor]]` utilisant l'Enum.
-   [x] **Choisir une taille/version de grille de référence :**
    -   [x] Taille de référence: Rayon approx. 10 (q/r de -10 à +10) - défini dans `constants.py` comme `GRID_RADIUS_REF`.
    -   Documenter ce choix temporaire. (Fait par commentaire dans `constants.py`)
-   [x] **Définir les positions centrales des 3 repères :**
    -   [x] Basé sur la taille de référence, déterminer 3 `AxialPos` pour les centres des repères.
        -   `FINDER_POS_TL: AxialPos = AxialPos(-8, 0)`
        -   `FINDER_POS_TR: AxialPos = AxialPos(0, -8)`
        -   `FINDER_POS_BL: AxialPos = AxialPos(-8, 8)`
    -   [x] Stocker ces positions comme constantes dans `constants.py`.
    -   *Note : Ces positions pourront être ajustées après visualisation.* 

## 2. Logique de Dessin

-   [x] **Créer le module de dessin :**
    -   [x] Créer un fichier `src/core/drawing.py` (ou nom similaire).
    -   [x] Ajouter les imports nécessaires (`ImageDraw` de PIL, les classes de `hex_grid`, les constantes de couleur).
-   [x] **Implémenter `draw_hexagon(draw: ImageDraw, hexagon: Hexagon, fill_color: tuple[int, int, int] | None, outline_color: tuple[int, int, int])` :**
    -   [x] Fonction utilitaire pour dessiner un seul hexagone avec une couleur de remplissage et/ou de contour.
    -   [x] Utilise `hexagon.get_vertices()`.
    -   [x] Convertit les `PixelCoord` en `tuple[float, float]` pour `draw.polygon()`.
-   [x] **Implémenter `draw_finder_pattern(draw: ImageDraw, layout: HexgridLayout, center_pos: AxialPos, pattern_type: Literal["origin", "yaxis"])` :**
    -   [x] Récupère les couleurs appropriées depuis `FINDER_COLORS`.
    -   [x] Crée l'hexagone central `center_hex = Hexagon(center_pos, layout)`.
    -   [x] Appelle `draw_hexagon` pour dessiner le centre avec `center_color`.
    -   [x] Récupère les 6 voisins : `neighbors = center_hex.get_neighbors()`.
    -   [x] Pour chaque `neighbor` dans `neighbors`, appelle `draw_hexagon` pour le dessiner avec `ring_color`.

## 3. Visualisation et Tests

-   [ ] **Mettre à jour le script de visualisation (`visualize_grid.py`) :**
    -   Importer les constantes de position (`FINDER_POS_TL`, etc.) et la fonction `draw_finder_pattern`.
    -   Après avoir dessiné la grille vide (ou les hexagones de base), appeler `draw_finder_pattern` trois fois avec les bonnes positions et types :
        -   `draw_finder_pattern(draw, layout, FINDER_POS_TL, "origin")`
        -   `draw_finder_pattern(draw, layout, FINDER_POS_TR, "origin")`
        -   `draw_finder_pattern(draw, layout, FINDER_POS_BL, "yaxis")`
    -   Exécuter le script et vérifier visuellement le résultat.
    -   Ajuster les `FINDER_POS_*` si nécessaire pour obtenir le placement souhaité des repères aux "coins".
-   [ ] **Tests Unitaires (Optionnel pour le dessin pur, mais recommandé si la logique devient complexe) :**
    -   Tester que `draw_finder_pattern` appelle bien `draw.polygon` le bon nombre de fois (7) avec les bonnes couleurs (difficile sans mocker `ImageDraw`).
    -   Se concentrer sur les tests des fonctions qui *calculent* les positions et les couleurs plutôt que sur le rendu pixel exact.

## Critères de Fin d'Étape

-   Les constantes de couleurs et de positions des repères sont définies.
-   Une fonction permet de dessiner un repère d'alignement complet à une position donnée.
-   Le script de visualisation montre correctement les 3 repères aux positions définies sur la grille.
